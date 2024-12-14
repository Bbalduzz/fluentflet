from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Union, TypeVar, Generic, Any
import flet as ft
from math import pi
from fluentflet.components import ListItem
from fluentflet.utils import FluentIcon, FluentIcons
from fluentflet.utils.fluent_design_system import FluentDesignSystem

T = TypeVar("T")


@dataclass
class TreeItemData:
    """Base data class for tree items"""

    id: str
    label: str
    value: Optional[Any] = None
    parent_id: Optional[str] = None
    children: List["TreeItemData"] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.metadata is None:
            self.metadata = {}


class TreeViewAbstractModel(ABC, Generic[T]):
    """
    Abstract model for tree view. example:
    class MyCustomModel(TreeViewAbstractModel[MyDataType]):
        def process_data(self):
            # Custom logic to convert self.raw_data into TreeItemData objects
            for item in self.raw_data:
                tree_item = TreeItemData(
                    id=item.id,
                    label=item.name,
                    value=item.data
                )
                self.add_item(tree_item)
    """

    def __init__(self):
        self.items: List[TreeItemData] = []
        self._raw_data: Optional[T] = None

    @property
    def raw_data(self) -> T:
        return self._raw_data

    @raw_data.setter
    def raw_data(self, value: T):
        self._raw_data = value
        self.items.clear()
        self.process_data()

    @abstractmethod
    def process_data(self):
        pass

    def get_item_by_id(self, item_id: str) -> Optional[TreeItemData]:
        return next((item for item in self.items if item.id == item_id), None)

    def get_root_items(self) -> List[TreeItemData]:
        return [item for item in self.items if item.parent_id is None]

    def get_children(self, parent_id: str) -> List[TreeItemData]:
        return [item for item in self.items if item.parent_id == parent_id]


class DictTreeViewModel(TreeViewAbstractModel[Dict]):
    def process_data(self):
        if not self.raw_data:
            return

        flat_dict = self._flatten_dict(self.raw_data)

        for path, value in flat_dict.items():
            parts = path.split(".")
            current_path = ""

            for i, part in enumerate(parts):
                current_path = f"{current_path}.{part}" if current_path else part
                parent_path = ".".join(parts[:i]) if i > 0 else None

                if not self.get_item_by_id(current_path):
                    is_leaf = i == len(parts) - 1
                    item = TreeItemData(
                        id=current_path,
                        label=f"{part}: {value}" if is_leaf else part,
                        value=value if is_leaf else None,
                        parent_id=parent_path,
                    )
                    self.items.append(item)

    @staticmethod
    def _flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(
                    DictTreeViewModel._flatten_dict(v, new_key, sep=sep).items()
                )
            else:
                items.append((new_key, v))
        return dict(items)


class JSONTreeViewModel(TreeViewAbstractModel[List[Dict]]):
    def __init__(self, field_mapping: Optional[Dict[str, str]] = None):
        super().__init__()
        default_mapping = {
            "id": "id",
            "label": "label",
            "value": "value",
            "children": "children",
        }
        if field_mapping:
            default_mapping.update(field_mapping)
        self.field_mapping = default_mapping
        self._id_counter = 0

    def _process_json_item(
        self, item: Dict, parent_id: Optional[str] = None, level: int = 0
    ) -> Optional[TreeItemData]:
        if not self._validate_item(item):
            return None

        item_id = str(self._get_field_value(item, "id") or self._generate_id())

        # Get custom fields
        custom_fields = {
            k: v for k, v in item.items() if k not in self.field_mapping.values()
        }

        tree_item = TreeItemData(
            id=item_id,
            label=self._get_field_value(item, "label", ""),
            value=self._get_field_value(item, "value"),
            parent_id=parent_id,
            children=[],
            metadata={"level": level, "raw_data": item, "custom_fields": custom_fields},
        )

        children = self._get_field_value(item, "children", [])
        for child in children:
            child_item = self._process_json_item(child, item_id, level + 1)
            if child_item:
                tree_item.children.append(child_item)

        return tree_item

    def _validate_item(self, item: Dict) -> bool:
        if not isinstance(item, dict):
            return False

        if not self._get_field_value(item, "label"):
            return False

        children = self._get_field_value(item, "children")
        if children is not None:
            if not isinstance(children, list):
                return False
            for child in children:
                if not self._validate_item(child):
                    return False

        return True

    def _get_field_value(self, item: Dict, field: str, default: Any = None) -> Any:
        mapped_field = self.field_mapping.get(field, field)
        return item.get(mapped_field, default)

    def _generate_id(self) -> str:
        self._id_counter += 1
        return f"generated_id_{self._id_counter}"

    def process_data(self):
        if not self.raw_data:
            return

        if not isinstance(self.raw_data, list):
            self.raw_data = [self.raw_data]

        self._id_counter = 0

        for item in self.raw_data:
            processed_item = self._process_json_item(item)
            if processed_item:
                self.items.append(processed_item)


class TreeView(ft.Column):
    def __init__(
        self,
        data: dict,
        model: Optional[TreeViewAbstractModel] = DictTreeViewModel(),
        on_right_click: callable = None,
        is_dark_mode: bool = True,
    ) -> None:
        super().__init__()
        self.model = model
        self.model.raw_data = data

        self.onRclick = on_right_click
        self.is_dark_mode = is_dark_mode
        self.nodes = []
        self.labels = {}
        self.expand = True
        self.scroll = ft.ScrollMode.ADAPTIVE

        self.create_tree_structure()

        self.controls = self.nodes
        self.alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.START

    def handle_item_drop(self, src_id: str, target_id: str):
        """Handle the reorganization of items when one is dropped onto another"""
        source_item = self.model.get_item_by_id(src_id)
        target_item = self.model.get_item_by_id(target_id)

        if source_item and target_item and source_item.parent_id != target_id:
            # Update the parent_id of the source item
            source_item.parent_id = target_id

            # Rebuild the tree structure
            self.nodes.clear()
            self.labels.clear()
            self.create_tree_structure()

            # Update the UI
            self.update()

    def create_tree_structure(self):
        # Create all nodes first
        for item in self.model.items:
            node = DraggableCollapsible(
                item_data=item,
                on_right_click=self.onRclick,
                is_dark_mode=self.is_dark_mode,
                tree_view=self,
            )
            self.labels[item.id] = node

        # Then establish parent-child relationships
        for node in self.labels.values():
            if node.item_data.parent_id is None:
                self.nodes.append(node)
                continue

            parent = self.labels.get(node.item_data.parent_id)
            if parent:
                parent.addChild(node)


class DraggableCollapsible(ft.Column):
    def __init__(
        self,
        item_data: TreeItemData,
        on_right_click: callable = None,
        is_dark_mode: bool = True,
        tree_view: TreeView = None,
    ) -> None:
        super().__init__()
        self.item_data = item_data
        self.rClick = on_right_click
        self.title = item_data.label
        self.code = item_data.id
        self.expanded = False
        self.expand = True
        self.is_dark_mode = is_dark_mode
        self.childColapsibles = []
        self.tree_view = tree_view

        self.chevron = ft.Container(
            content=FluentIcon(FluentIcons.CHEVRON_RIGHT, size=10, color="#ffffff"),
            rotate=0,
            animate_rotation=200,
        )

        # Create header row with icon and text
        header_row = ft.Row(
            controls=[
                self.chevron if not self.item_data.value else ft.Container(width=24),
                ft.Text(self.title, size=14),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Create ListItem for the header
        self.list_item = ListItem(
            content=header_row,
            on_click=self.handle_click,
            is_dark_mode=self.is_dark_mode,
        )

        # Only make it draggable if it's not a root item
        if self.item_data.parent_id is not None:
            self.list_item = ft.Draggable(
                group="tree_items",
                content=self.list_item,
                content_feedback=ft.Container(
                    content=ft.Text(self.title, color=ft.Colors.WHITE, size=14),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    padding=3,
                    border_radius=5,
                ),
                data=self.code,
            )

        # Make all items drop targets
        self.drag_target = ft.DragTarget(
            group="tree_items",
            content=self.list_item,
            on_will_accept=self.on_will_accept,
            on_accept=self.on_accept,
            on_leave=self.on_leave,
        )

        # Children container
        self.children_container = ft.Container(
            content=ft.Column(controls=[], spacing=0),
            animate_opacity=200,
            animate_offset=ft.animation.Animation(200, "easeOut"),
            offset=ft.transform.Offset(0, -0.5),
            opacity=0,
            clip_behavior=ft.ClipBehavior.NONE,
            visible=False,
        )

        self.controls = [self.drag_target, self.children_container]
        self.spacing = 0
        self.spacer = ft.Container(width=28, padding=ft.padding.only(left=4))

        if self.item_data.value is not None:
            self.chevron.visible = False

    def addChild(self, child: ft.Column) -> None:
        self.childColapsibles.append(child)

        indented_child = ft.Row(
            controls=[self.spacer, child],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        if len(self.childColapsibles) == 1:
            self.chevron.visible = True

        self.children_container.content.controls.append(indented_child)

    def handle_click(self, e) -> None:
        if self.childColapsibles:
            self.expanded = not self.expanded
            if not self.expanded:
                self.children_container.offset = ft.transform.Offset(0, -0.5)
                self.children_container.opacity = 0
                self.children_container.visible = False
            else:
                self.children_container.offset = ft.transform.Offset(0, 0)
                self.children_container.opacity = 1
                self.children_container.visible = True
            self.chevron.rotate = pi / 2 if self.expanded else 0
            self.children_container.update()
            self.chevron.update()

    def on_will_accept(self, e):
        # Don't allow dropping onto leaf nodes (items with values)
        if self.item_data.value is not None:
            e.control.content.border = ft.border.all(2, ft.colors.ERROR)
            e.control.update()
            return

        e.control.content.border = ft.border.all(
            2, ft.colors.SURFACE_VARIANT if e.data == "true" else ft.colors.ERROR
        )
        e.control.update()

    def on_accept(self, e):
        if self.item_data.value is not None:
            return

        # Reset border
        e.control.content.border = None
        e.control.update()

        # Use the TreeView's handle_item_drop directly
        if self.tree_view:
            self.tree_view.handle_item_drop(e.src_id, self.code)

    def on_leave(self, e):
        e.control.content.border = None
        e.control.update()
