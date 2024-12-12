<p align="center">
  <img width="50%" align="center" src="https://github.com/user-attachments/assets/01fcda49-a016-47c7-949f-83f35e47bd35" alt="logo">
</p>
<p align="center">
  <img width="10%" align="center" src="https://github.com/user-attachments/assets/49d157d1-0893-4b81-a812-794e41a2b0a8" alt="logo">
</p>

<h1 align="center">
  Fluent Flet
</h1>

<p align="center">
  A fluent design widgets library based on Flet 
</p>

<div align="center">
    <kbd>
      <video width="100%" align="center" src="https://github.com/user-attachments/assets/5952ce87-d679-411e-a050-e58776d1764b" alt="demo">
    </kbd>
</div>

<h1 align="left">
  Documentation
  <img src="https://img.shields.io/badge/prerelease-8FD28F" alt="logo">
</h1>

<details>
<summary>Table of Contents</summary>

#### Components
- [Button](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#button-component)
  - [ButtonVariant](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#buttonvariant-enum)
  - [Button](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#button)
- [Checkbox](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#checkbox-component) 
  - [CheckState](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#checkstate-enum)
  - [Checkbox](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#checkbox)
- [Dialog](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#dialog-component)
  - [Dialog](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#dialog)
- [Dropdown](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#dropdown-component)
  - [Dropdown](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#dropdown)
- [Expander](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#expander-component)
  - [Expander](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#expander)
- [ListItem](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#listitem-component)
  - [ListItem](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#listitem)
- [ProgressRing](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#progressring-component) 
  - [ProgressRing](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#progressring)
- [Radio](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#radio-component)
  - [Radio](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#radio)
  - [RadioGroup](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#radiogroup)
- [Slider](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#slider-component)
  - [SliderOrientation](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#sliderorientation-enum)
  - [Slider](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#slider)
- [TextBox](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#textbox-component)
  - [TextBox](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#textbox)
- [Toggle](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toggle-component)
  - [Toggle](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toggle) 
- [Tooltip](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#tooltip-component)
  - [Tooltip](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#tooltip)
- [TreeView](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#treeview-components)
  - [TreeItemData](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#treeitemdata) 
  - [TreeViewAbstractModel](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#treeviewabstractmodel)
  - [DictTreeViewModel](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#dicttreeviewmodel)
  - [JSONTreeViewModel](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#jsontreeviewmodel)
  - [TreeView](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#treeview)
- [Toast](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toast-component)
  - [Enums](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#enums)
    - [ToastPosition](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toastposition)
    - [ToastVariant](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toastvariant) 
    - [ToastSeverity](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toastseverity)
    - [ToastActionType](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toastactiontype)
  - [Toast](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toast)
  - [Toaster](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#toaster)

#### Enhancements  
- [Page Monkey Patches](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#page-monkey-patches)
- [FluentWindow](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#fluentwindow)
  - [FluentState](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#fluentstate)
  - [FluentWindow](https://github.com/Bbalduzz/fluentflet?tab=readme-ov-file#fluentwindow-1)
</details>

## Button Component
> `fluentflet/components/button.py`

### ButtonVariant (Enum)
```python
class ButtonVariant(Enum):
    DEFAULT = "default"     # Standard button styling
    ACCENT = "accent"       # Primary action/emphasized styling
    HYPERLINK = "hyperlink" # Text-like button styling 
    TOGGLE = "toggle"       # Toggleable state button
```

### Button
**Purpose**: Implements Fluent Design System button control with multiple variants and styles.
**Inherits from**: `ft.TextButton`

#### Attributes:
- `is_toggled: bool = False`. Current toggle state for toggle variant buttons
- `_variant: ButtonVariant`. Current button style variant
- `design_system: FluentDesignSystem`. Reference to design system for styling
- `theme: Theme`. Current theme settings

#### Constructor Parameters:
- `content: Union[str, ft.Control] = None`. Button content (text or control like icon)
  - If string: Creates Text control automatically
  - If control: Uses directly
- `variant: ButtonVariant = ButtonVariant.DEFAULT`. Button style variant
- `height: int = 35`. Button height in pixels
- `custom_color: Optional[str] = None`. Optional color override
- `design_system: FluentDesignSystem = None`. Design system instance
- `is_dark_mode: bool = True`. Theme mode selection
- `**kwargs`. Additional Flet button properties

#### Example Usage:
```python
from fluentflet.components import Button, ButtonVariant
from fluentflet.utils import FluentIcon, FluentIcons

# Text button
basic_button = Button(
    "Click Me", 
    variant=ButtonVariant.DEFAULT,
    on_click=lambda e: print("Clicked!")
)

# Icon button with accent
icon_button = Button(
    content=FluentIcon(FluentIcons.ADD), 
    variant=ButtonVariant.ACCENT
)

# Toggle button
toggle = Button(
    "Toggle Me",
    variant=ButtonVariant.TOGGLE,
    on_click=lambda e: print(f"Toggled: {toggle.is_toggled}")
)
```

## Checkbox Component
**Path**: `fluentflet/components/checkbox.py`

### CheckState (Enum)
```python
class CheckState(Enum):
    UNCHECKED = "unchecked"       # Box is empty
    CHECKED = "checked"           # Box has checkmark
    INDETERMINATE = "indeterminate" # Box has dash (mixed state)
```

### Checkbox
**Purpose**: Implements tri-state checkbox control with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Attributes:
- `state: CheckState`. Current checkbox state
- `_disabled: bool`. Disabled state tracking
- `size: int`. Size of the checkbox in pixels
- `three_state: bool`. Whether indeterminate state is allowed

#### Constructor Parameters:
- `state: CheckState = CheckState.UNCHECKED`. Initial state
- `label: str = ""`. Optional label text
- `size: int = 20`. Size in pixels
- `on_change: Callable[[CheckState], None] = None`. State change callback
- `disabled: bool = False`. Initial disabled state
- `three_state: bool = False`. Enable tri-state behavior
- `design_system: FluentDesignSystem = None`. Design system instance 
- `is_dark_mode: bool = True`. Theme mode
- `**kwargs`. Additional container properties

#### Example Usage:
```python
from fluentflet.components import Checkbox, CheckState

# Basic checkbox
checkbox = Checkbox(
    label="Enable feature",
    on_change=lambda state: print(f"State: {state}")
)

# Tri-state checkbox
tristate = Checkbox(
    label="Select files",
    three_state=True,
    state=CheckState.INDETERMINATE
)

# Disabled checkbox 
disabled = Checkbox(
    label="Unavailable option",
    disabled=True,
    state=CheckState.CHECKED
)
```

## Dialog Component
> `fluentflet/components/dialog.py`

### Dialog
**Purpose**: Implements a modal dialog overlay with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Attributes:
- `dialog_width: int = 400`. Width of dialog in pixels 
- `title_text: str`. Dialog title
- `_content: ft.Control`. Main dialog content
- `actions: List[Button]`. Action buttons for dialog

#### Constructor Parameters:
- `title: str = "Dialog Title"`. Dialog header text
- `content: Optional[ft.Control] = None`. Main content area
  - Defaults to simple text if not provided
  - Can be any Flet control
- `actions: Optional[List[Button]] = None`. Bottom action buttons
  - Defaults to ["Action", "Close"] buttons if not provided
  - Close button automatically included

#### Methods:
- `show()`: Display the dialog
  ```python
  Returns:
  - None: Updates page overlay
  ```

- `close_dialog(e: Optional[ft.ControlEvent] = None)`: Hide and remove dialog
  ```python
  Returns:
  - None: Removes from page overlay
  ```

#### Example Usage:
```python
from fluentflet.components import Dialog, Button, ButtonVariant

# Simple dialog
dialog = Dialog(
    title="Confirm Action",
    content=ft.Text("Are you sure you want to proceed?")
)

# Custom dialog with multiple actions
custom_dialog = Dialog(
    title="Save Changes",
    content=ft.Column([
        ft.Text("Save current changes?"),
        ft.TextField(label="Comment")
    ]),
    actions=[
        Button("Save", variant=ButtonVariant.ACCENT),
        Button("Don't Save"),
        Button("Cancel")
    ]
)

# Show dialog
page.overlay.append(dialog)
dialog.show()
```

## Dropdown Component
> `fluentflet/components/dropdown.py`

### Dropdown
**Purpose**: Implements a dropdown select control with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Attributes:
- `options: List[Union[str, ft.Control]]`. Available options
- `max_width: int`. Maximum width of dropdown
- `selected_value: str`. Currently selected option
- `is_open: bool`. Dropdown expanded state

#### Constructor Parameters:
- `options: List[Union[str, ft.Control]]`. List of dropdown options
  - Can be strings or Flet controls
  - Must not be empty
- `max_width: int = 150`. Maximum width in pixels
- `theme_mode: ft.ThemeMode = ft.ThemeMode.DARK`. Theme selection
- `on_select: Optional[Callable] = None`. Selection change callback
- `animated: bool = True`. Enable animations
- `initial_value: Optional[str] = None`. Initially selected item
- `**kwargs`. Additional container properties

#### Example Usage:
```python
from fluentflet.components import Dropdown

# Simple string options
dropdown = Dropdown(
    options=["Option 1", "Option 2", "Option 3"],
    on_select=lambda value: print(f"Selected: {value}")
)

# Custom control options
dropdown_with_icons = Dropdown(
    options=[
        ft.Row([
            ft.Icon(ft.icons.SETTINGS),
            ft.Text("Settings")
        ]),
        ft.Row([
            ft.Icon(ft.icons.PERSON),
            ft.Text("Profile")
        ])
    ],
    max_width=200
)
```

## Expander Component  
> `fluentflet/components/expander.py`

### Expander
**Purpose**: Implements collapsible/expandable section with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Attributes:
- `_expanded: bool`. Current expansion state
- `_width: int`. Width of expander
- `_header: ft.Control`. Header content 
- `_content: ft.Control`. Main content
- `_content_height: Optional[int]`. Cached content height for animation

#### Constructor Parameters:
- `header: Union[str, ft.Control]`. Content shown in always-visible header
  - If string: Creates text control
  - If control: Uses directly
- `content: ft.Control`. Content shown when expanded
- `expand: bool = False`. Initial expanded state
- `width: int = 600`. Expander width in pixels
- `is_dark_mode: bool = True`. Theme mode
- `**kwargs`. Additional container properties

#### Properties:
- `expanded: bool`. Get/set expanded state

#### Example Usage:
```python
from fluentflet.components import Expander

# Simple text expander
expander = Expander(
    header="Click to Expand",
    content=ft.Text("Expanded content here"),
    expand=False
)

# Complex expander with custom header
expander = Expander(
    header=ft.Row([
        ft.Icon(ft.icons.SETTINGS),
        ft.Text("Advanced Settings")
    ]),
    content=ft.Column([
        ft.TextField(label="Setting 1"),
        ft.TextField(label="Setting 2")
    ])
)
```

## ListItem Component
> `fluentflet/components/listitem.py`

### ListItem
**Purpose**: Implements selectable list item with Fluent Design styling.
**Inherits from**: `ft.GestureDetector`

#### Class Attributes:
- `instances: List[ListItem]`. All created instances for selection management

#### Instance Attributes:
- `item_content: ft.Control`. Item's content
- `is_hovered: bool`. Hover state
- `is_pressed: bool`. Press state
- `_is_selected: bool`. Selection state

#### Constructor Parameters:
- `content: ft.Control`. Item content
- `on_click: Optional[Callable] = None`. Click handler
- `is_dark_mode: bool = True`. Theme mode
- `selected: bool = False`. Initial selection state
- `**kwargs`. Additional gesture detector properties

#### Properties:
- `selected: bool`. Get/set selection state

#### Example Usage:
```python
from fluentflet.components import ListItem

# Simple list item
item = ListItem(
    content=ft.Text("List Item 1"),
    on_click=lambda _: print("Clicked")
)

# Complex list item
item = ListItem(
    content=ft.Row([
        ft.Icon(ft.icons.PERSON),
        ft.Column([
            ft.Text("John Doe"),
            ft.Text("john@example.com", size=12)
        ])
    ]),
    selected=True
)

# List of items
items_list = ft.ListView(
    controls=[
        ListItem(content=ft.Text(f"Item {i}"))
        for i in range(5)
    ]
)
```

## ProgressRing Component
> `fluentflet/components/progressring.py`

### ProgressRing
**Purpose**: Implements circular progress indicator with Fluent Design styling.
**Inherits from**: `ft.ProgressRing`

#### Constructor Parameters:
- `stroke_width: int = 3`. Width of the ring stroke
- `value: Optional[float] = None`. Progress value (0.0-1.0 for determinate, None for indeterminate)
- `**kwargs`. Additional progress ring properties

#### Example Usage:
```python
from fluentflet.components import ProgressRing

# Indeterminate progress
loading = ProgressRing()

# Determinate progress
progress = ProgressRing(value=0.75)

# Custom styled progress
custom = ProgressRing(
    value=0.5,
    stroke_width=5,
    width=100,
    height=100
)
```

## Radio Component
>`fluentflet/components/radio.py`

### Radio
**Purpose**: Implements individual radio button control.
**Inherits from**: `ft.Container`

#### Attributes:
- `value: Any`. Value associated with radio button
- `_selected: bool`. Current selection state
- `_disabled: bool`. Disabled state
- `is_hovered: bool`. Hover state
- `is_pressed: bool`. Press state
- `_radio_group: Optional[RadioGroup]`. Parent radio group

#### Constructor Parameters:
- `value: Any = None`. Value for this radio option
- `label: str = ""`. Label text
- `selected: bool = False`. Initial selection
- `disabled: bool = False`. Disabled state
- `design_system: FluentDesignSystem = None`. Design system instance
- `is_dark_mode: bool = True`. Theme mode
- `**kwargs`. Additional container properties

### RadioGroup
**Purpose**: Container for managing a group of related radio buttons.

**Inherits from**: `ft.Container`

#### Attributes:
- `radios: List[Radio]`. Child radio buttons
- `_value: Any`. Currently selected value
- `_on_change: Optional[Callable]`. Value change callback

#### Constructor Parameters:
- `content: ft.Control = None`. Container content
- `value: Any = None`. Initial selected value
- `on_change: Optional[Callable] = None`. Value change handler
- `design_system: FluentDesignSystem = None`. Design system instance
- `is_dark_mode: bool = True`. Theme mode
- `**kwargs`. Additional container properties

#### Example Usage:
```python
from fluentflet.components import Radio, RadioGroup

# Single radio button
radio = Radio(
    value="option1",
    label="Option 1",
    disabled=False
)

# Radio group
radio_group = RadioGroup(
    content=ft.Column([
        Radio(value="small", label="Small"),
        Radio(value="medium", label="Medium"),
        Radio(value="large", label="Large")
    ]),
    value="medium",
    on_change=lambda value: print(f"Selected: {value}")
)
```

## Slider Component
> `fluentflet/components/slider.py`

### SliderOrientation (Enum)
```python
class SliderOrientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
```

### Slider
**Purpose**: Implements a draggable slider control with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Attributes:
- `current_value: float`. Current slider value
- `min: float`. Minimum value
- `max: float`. Maximum value
- `dragging: bool`. Current drag state
- `thumb_size: int`. Size of slider thumb
- `is_hovered: bool`. Hover state
- `is_pressed: bool`. Press state

#### Constructor Parameters:
- `value: float = 0`. Initial value
  - Must be between min and max
- `min: float = 0`. Minimum value
- `max: float = 100`. Maximum value
- `on_change: Optional[Callable[[float], None]] = None`. Value change callback
- `size: int = 200`. Slider length in pixels
- `disabled: bool = False`. Disabled state
- `orientation: SliderOrientation = SliderOrientation.HORIZONTAL`. Slider orientation
- `is_dark_mode: bool = True`. Theme mode
- `**kwargs`. Additional container properties

#### Example Usage:
```python
from fluentflet.components import Slider, SliderOrientation

# Horizontal slider
slider = Slider(
    value=50,
    min=0,
    max=100,
    on_change=lambda e: print(f"Value: {e.current_value}")
)

# Vertical slider
vertical_slider = Slider(
    value=0.5,
    min=0,
    max=1,
    orientation=SliderOrientation.VERTICAL,
    size=150
)

# Custom range slider
custom = Slider(
    value=-50,
    min=-100,
    max=100,
    disabled=False
)
```

## TextBox Component
> `fluentflet/components/textbox.py`

### TextBox
**Purpose**: Implements text input control with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Attributes:
- `textfield: ft.TextField`. Core text input control
- `bottom_border: ft.Container`. Bottom border with animation
- `actions_row: ft.Row`. Container for action buttons
- `default_bgcolor: str`. Default background color

#### Constructor Parameters:
- `design_system: FluentDesignSystem = FluentDesignSystem()`. Design system instance
- `placeholder: str = "TextBox"`. Placeholder text
- `width: int = 200`. Control width
- `text_size: int = 14`. Font size
- `height: int = 32`. Control height
- `password: bool = False`. Password input mode
- `actions_visible: bool = True`. Show/hide action buttons
- `**kwargs`. Additional container properties

#### Methods:
- `add_action(icon: FluentIcons, on_click=None, tooltip: str = None) -> Button`
  - Adds action button to textbox
  - Returns the created button

#### Example Usage:
```python
from fluentflet.components import TextBox
from fluentflet.utils import FluentIcons

# Basic textbox
textbox = TextBox(
    placeholder="Enter text",
    width=300
)

# Password textbox
password = TextBox(
    placeholder="Password",
    password=True
)

# Textbox with actions
textbox_with_actions = TextBox(
    placeholder="Search",
    width=400
)
textbox_with_actions.add_action(
    icon=FluentIcons.SEARCH,
    on_click=lambda _: print("Search clicked"),
    tooltip="Search"
)
textbox_with_actions.add_action(
    icon=FluentIcons.DISMISS,
    on_click=lambda _: setattr(textbox_with_actions, 'value', ''),
    tooltip="Clear"
)
```

## Toggle Component
> `fluentflet/components/toggle.py`

### Toggle
**Purpose**: Implements a toggle switch with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Attributes:
- `value: bool`. Current toggle state
- `on_content: str`. Label text for ON state
- `off_content: str`. Label text for OFF state
- `_label: str`. Current label text
- `_handle_size: int`. Size of toggle handle
- `_handle_expanded_width: int`. Width when handle is pressed

#### Constructor Parameters:
- `value: bool = False`. Initial state
- `label: Union[str, dict] = None`. Label text or dict with on/off states
  - If string: Same label for both states
  - If dict: Must have "on_content" and "off_content" keys
- `label_position: ft.LabelPosition = ft.LabelPosition.RIGHT`. Label placement
- `on_change: Optional[Callable[[bool], None]] = None`. State change callback
- `label_style: Optional[Dict] = None`. Label text styling
- `disabled: bool = False`. Disabled state
- `width: int = 40`. Toggle width
- `height: int = 20`. Toggle height
- `**kwargs`. Additional container properties

#### Example Usage:
```python
from fluentflet.components import Toggle

# Simple toggle
toggle = Toggle(
    value=False,
    label="Enable feature",
    on_change=lambda state: print(f"Toggled: {state}")
)

# Toggle with different labels
toggle = Toggle(
    value=True,
    label={
        "on_content": "Enabled",
        "off_content": "Disabled"
    }
)

# Custom styled toggle
toggle = Toggle(
    label="Custom toggle",
    label_style={
        "size": 16,
        "weight": "bold"
    },
    width=50,
    height=25
)
```

## Tooltip Component
> `fluentflet/components/tooltip.py`

### ToolTip
**Purpose**: Implements hover tooltip with Fluent Design styling.
**Inherits from**: `ft.Tooltip`

#### Constructor Parameters:
- `padding: int = 6`. Tooltip padding
- `border_radius: int = 4`. Corner radius
- `text_style: ft.TextStyle`. Tooltip text styling
- `bgcolor: str = "#2d2d2d"`. Background color
- `border: ft.Border`. Border style
- `prefer_below: bool = False`. Show below target when possible
- `wait_duration: int = 300`. Delay before showing (ms)
- `**kwargs`. Additional tooltip properties

#### Example Usage:
```python
from fluentflet.components import ToolTip, Button

# Basic tooltip
button = Button("Hover me")
tooltip = ToolTip(
    message="This is a tooltip",
    content=button
)

# Custom styled tooltip
tooltip = ToolTip(
    message="Custom tooltip",
    content=ft.Text("Hover for info"),
    text_style=ft.TextStyle(
        size=14,
        weight=ft.FontWeight.BOLD
    ),
    bgcolor="#333333",
    border_radius=8
)
```

## TreeView Components
> `fluentflet/components/treeview.py`

### TreeItemData
**Purpose**: Base data structure for tree items.

#### Attributes:
- `id: str`. Unique identifier for the item
- `label: str`. Display text
- `value: Optional[Any] = None`. Associated value
- `parent_id: Optional[str] = None`. ID of parent item
- `children: List[TreeItemData] = None`. Child items
- `metadata: Dict[str, Any] = None`. Additional item data

#### Example Usage:
```python
item = TreeItemData(
    id="root",
    label="Root Item",
    children=[
        TreeItemData(id="child1", label="Child 1"),
        TreeItemData(id="child2", label="Child 2")
    ]
)
```

### TreeViewAbstractModel
**Purpose**: Abstract base class for tree data models.
**Generic Type**: `T` - Type of raw data

#### Attributes:
- `items: List[TreeItemData]`. Processed tree items
- `_raw_data: Optional[T]`. Source data

#### Abstract Methods:
- `process_data()`: Convert raw data to TreeItemData objects

#### Common Methods:
- `get_item_by_id(item_id: str) -> Optional[TreeItemData]`
- `get_root_items() -> List[TreeItemData]`
- `get_children(parent_id: str) -> List[TreeItemData]`

### DictTreeViewModel
**Purpose**: Tree model for dictionary data.
**Inherits from**: `TreeViewAbstractModel[Dict]`

#### Example Usage:
```python
data = {
    "Root": {
        "Child1": {
            "GrandChild1": 1.1,
            "GrandChild2": 1.2
        },
        "Child2": 2.0
    }
}

model = DictTreeViewModel()
model.raw_data = data
```

### JSONTreeViewModel
**Purpose**: Tree model for JSON array/object data.
**Inherits from**: `TreeViewAbstractModel[List[Dict]]`

#### Constructor Parameters:
- `field_mapping: Optional[Dict[str, str]] = None`. Custom field name mapping
  - Default maps: id, label, value, children

#### Example Usage:
```python
data = [
    {
        "id": "1",
        "label": "Item 1",
        "children": [
            {
                "id": "1.1",
                "label": "Subitem 1.1"
            }
        ]
    }
]

model = JSONTreeViewModel()
model.raw_data = data
```

### TreeView
**Purpose**: Main tree view component with drag-drop support.
**Inherits from**: `ft.Column`

#### Constructor Parameters:
- `data: dict`. Source data
- `model: Optional[TreeViewAbstractModel] = DictTreeViewModel()`. Data model
- `on_right_click: Optional[Callable] = None`. Right-click handler
- `is_dark_mode: bool = True`. Theme mode

#### Methods:
- `handle_item_drop(src_id: str, target_id: str)`: Handle item reordering

#### Example Usage:
```python
from fluentflet.components import TreeView, DictTreeViewModel

# Basic tree
data = {
    "Root": {
        "Item1": 1.0,
        "Item2": {
            "SubItem1": 2.1,
            "SubItem2": 2.2
        }
    }
}

tree = TreeView(
    data=data,
    model=DictTreeViewModel(),
    on_right_click=lambda item: print(f"Right clicked: {item.label}")
)

# Custom model tree
class MyModel(TreeViewAbstractModel[List[Dict]]):
    def process_data(self):
        for item in self.raw_data:
            self.items.append(TreeItemData(
                id=str(item["id"]),
                label=item["name"],
                value=item["data"]
            ))

tree = TreeView(
    data=my_data,
    model=MyModel()
)
```

## Toast Component
> `fluentflet/components/toast.py`

### Enums

#### ToastPosition
```python
class ToastPosition(Enum):
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    TOP_CENTER = "top-center"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"
    BOTTOM_CENTER = "bottom-center"
```

#### ToastVariant
```python
class ToastVariant(Enum):
    SINGLE_LINE = "single-line"  # Compact single line toast
    MULTI_LINE = "multi-line"    # Expanded multi-line toast
```

#### ToastSeverity
```python
class ToastSeverity(Enum):
    INFORMATIONAL = "informational"  # Blue info style
    SUCCESS = "success"              # Green success style
    WARNING = "warning"              # Yellow warning style
    CRITICAL = "critical"            # Red error style
```

#### ToastActionType
```python
class ToastActionType(Enum):
    NONE = "none"          # No action button
    HYPERLINK = "hyperlink"  # Link style action
    DEFAULT = "default"      # Button style action
```

### Toast
**Purpose**: Individual toast notification with Fluent Design styling.
**Inherits from**: `ft.Container`

#### Constructor Parameters:
- `title: Optional[str] = None`. Toast title text
- `message: Optional[str] = None`. Toast message text
- `severity: ToastSeverity | str = ToastSeverity.INFORMATIONAL`. Toast style
- `variant: ToastVariant | str = ToastVariant.SINGLE_LINE`. Layout style
- `action_type: ToastActionType | str = ToastActionType.NONE`. Action button type
- `action_text: Optional[str] = None`. Action button text
- `action_url: Optional[str] = None`. URL for hyperlink action
- `on_action: Optional[Callable] = None`. Action click handler
- `position: ToastPosition | str = ToastPosition.TOP_RIGHT`. Toast position
- `**kwargs`. Additional container properties

### Toaster
**Purpose**: Toast notification manager for showing/hiding toasts.

#### Constructor Parameters:
- `page: ft.Page`. Flet page instance
- `expand: bool = False`. Auto-expand toasts on hover
- `position: ToastPosition | str = ToastPosition.TOP_RIGHT`. Default position
- `theme: str = "dark"`. Theme mode
- `default_toast_duration: int = 3`. Default show duration in seconds
- `default_offset: int = 20`. Spacing from window edge

#### Methods:

#### show_toast
```python
def show_toast(
    self,
    title: Optional[str] = None,
    message: Optional[str] = None,
    severity: ToastSeverity | str = ToastSeverity.INFORMATIONAL,
    variant: ToastVariant | str = ToastVariant.SINGLE_LINE,
    action_type: ToastActionType | str = ToastActionType.NONE,
    action_text: Optional[str] = None,
    action_url: Optional[str] = None,
    on_action: Optional[Callable] = None,
    position: Optional[ToastPosition | str] = None,
    duration: int = 3,
    toast: Optional[Toast] = None,
    **kwargs
) -> None
```

#### Example Usage:
```python
from fluentflet.components import Toast, Toaster, ToastSeverity

def main(page: ft.Page):
    # Create toaster
    toaster = Toaster(
        page=page,
        position="top-right",
        default_toast_duration=5
    )

    # Show simple toast
    toaster.show_toast(
        title="Success!",
        message="Operation completed",
        severity=ToastSeverity.SUCCESS
    )

    # Show toast with action
    toaster.show_toast(
        title="Warning",
        message="Connection lost",
        severity=ToastSeverity.WARNING,
        action_type="default",
        action_text="Retry",
        on_action=lambda: print("Retrying...")
    )

    # Show custom toast
    custom_toast = Toast(
        title="Custom Toast",
        message="With custom styling",
        severity=ToastSeverity.INFORMATIONAL,
        variant=ToastVariant.MULTI_LINE,
        action_type=ToastActionType.HYPERLINK,
        action_text="Learn More",
        action_url="https://example.com"
    )
    toaster.show_toast(toast=custom_toast)

ft.app(target=main)
```

The Toast system provides:
- Multiple severity levels with appropriate styling
- Single and multi-line variants
- Custom action buttons/links
- Flexible positioning
- Automatic stacking and animation
- Hover expansion
- Duration control

---

# Enhancements
## Page Monkey Patches
> `fluentflet/utils/__init__.py`

**Purpose**: Extends Flet's Page class with additional functionality for blur effects and drag-drop support.

### Added Page Properties

#### page.`blur_effect`
```python
@property
def blur_effect(self) -> bool:
    """Controls window blur effect on Windows"""
    return self._blur

@blur_effect.setter
def blur_effect(self, value: bool):
    # Only available on Windows
    # Enables/disables acrylic blur effect
```

#### page.`accepts_drops`
```python
@property
def accepts_drops(self) -> bool:
    """Controls file drop acceptance"""
    return self._accepts_drops

@accepts_drops.setter
def accepts_drops(self, value: bool):
    # Enables/disables file drop handling
```

### Added Page Methods

#### enable_drag_and_drop
```python
def enable_drag_and_drop(
    files_callback: Optional[Callable[[List[str]], None]] = None,
    drag_enter_callback: Optional[Callable[[Tuple[int, int]], None]] = None,
    drag_over_callback: Optional[Callable[[Tuple[int, int]], None]] = None,
    drag_leave_callback: Optional[Callable[[], None]] = None
):
    """Enable file drag-drop functionality
    
    Parameters:
    - files_callback: Called with list of dropped file paths
    - drag_enter_callback: Called with (x,y) when drag enters window
    - drag_over_callback: Called with (x,y) while dragging over window
    - drag_leave_callback: Called when drag leaves window
    """
```

Example Usage:
```python
def on_files_dropped(files):
    print("Files dropped:", files)

def on_drag_enter(point):
    print(f"Drag entered at {point}")

page.accepts_drops = True
page.enable_drag_and_drop(
    files_callback=on_files_dropped,
    drag_enter_callback=on_drag_enter
)
```

## FluentWindow
> `fluentflet/window/fluent_window.py`

**Purpose**: Implements a window manager with navigation, routing and state management following Fluent Design.

### Classes

#### FluentState
**Purpose**: State management for FluentWindow applications

```python
class FluentState:
    """Manages persistent and ephemeral application state"""
    
    def set(self, key: str, value: any, persist: bool = False):
        """Set state value
        
        Parameters:
        - key: State key
        - value: State value
        - persist: If True, saves to session storage
        """
        
    def get(self, key: str, default=None) -> any:
        """Get state value"""
        
    def subscribe(self, key: str, callback: callable):
        """Subscribe to state changes"""
```

Example Usage:
```python
class AppState(FluentState):
    def _load_initial_state(self):
        self._state = {
            "theme": "light",
            "selected_user": None
        }
    
    def set_theme(self, theme: str):
        self.set("theme", theme, persist=True)

window.state = AppState()
window.state.subscribe("theme", lambda t: print(f"Theme changed: {t}"))
```

#### FluentWindow
**Purpose**: Main window manager implementing navigation and routing

##### Constructor Parameters:
- `page: ft.Page`. Flet page instance
- `navigation_items: Optional[List[Dict]]`. Navigation menu items
  ```python
  [
      {
          "icon": FluentIcons.HOME,  # Icon enum
          "label": "Home",           # Display text 
          "route": "/",              # Optional route
      }
  ]
  ```
- `bottom_navigation_items: Optional[List[Dict]]`. Bottom nav items
- `selected_index: int = 0`. Initial selected nav item
- `window_titlebar: Union[str, Titlebar]`. Window title or titlebar component
- `colors: Optional[Dict]`. Color overrides
  ```python
  {
      "nav_bg": "#1F1F1F",
      "content_bg": "#282828",
      "title_bar_bg": "#1F1F1F",
      "icon_color": "white",
      "text_color": "white" 
  }
  ```
- `nav_width_collapsed: int = 50`. Navigation width when collapsed
- `nav_width_expanded: int = 200`. Navigation width when expanded
- `animation_duration: int = 100`. Animation duration in ms
- `show_back_button: bool = True`. Show navigation back button
- `state_manager: Type[FluentState] = FluentState`. State manager class

##### Methods:

###### Navigation
```python
def navigate(self, route: str, **params):
    """Navigate to route with optional parameters
    
    Parameters:
    - route: Route path
    - **params: Route parameters
    """

@route("/path")
def view_builder():
    """Route decorator for registering views"""
    return ft.Column([...])

def add_route(self, route: str, view_builder: Callable[..., ft.Control], 
              is_template: bool = False):
    """Register route manually"""
```

Example Usage:
```python
def main(page: ft.Page):
    window = FluentWindow(
        page,
        navigation_items=[
            {"icon": FluentIcons.HOME, "label": "Home", "route": "/"},
            {"icon": FluentIcons.PEOPLE, "label": "Users", "route": "/users"}
        ]
    )

    @window.route("/")
    def home_view():
        return ft.Column([
            ft.Text("Welcome!", size=32),
            Button("View Users", 
                  on_click=lambda _: window.navigate("/users"))
        ])

    @window.route("/users/:user_id", is_template=True)
    def user_profile(user_id: str):
        return ft.Column([
            ft.Text(f"User Profile: {user_id}")
        ])

    window.navigate("/")

ft.app(target=main)
```

Let me know if you need any clarification or have questions about specific functionality!
