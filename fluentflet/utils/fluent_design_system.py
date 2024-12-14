from dataclasses import dataclass, field
import flet as ft


@dataclass
class AccentColors:
    accent_light_3: str = "#FFB4D9"
    accent_light_2: str = "#62B6F7"
    accent_light_1: str = "#0078D4"
    accent_base: str = "#005FB8"
    accent_dark_1: str = "#004C99"
    accent_dark_2: str = "#003A77"
    accent_dark_3: str = "#002952"


@dataclass
class ControlProperties:
    control_corner_radius: int = 4
    overlay_corner_radius: int = 8
    control_slow_duration: int = 333
    control_normal_duration: int = 250
    control_fast_duration: int = 167
    control_faster_duration: int = 83


@dataclass
class FontFamilies:
    font_family_fallback: str = (
        '"Segoe UI", -apple-system, ui-sans-serif, system-ui, BlinkMacSystemFont, Helvetica, Arial, sans-serif'
    )
    font_family_text: str = (
        '"Segoe UI Variable Text", "Seoge UI Variable Static Text", var(--fds-font-family-fallback)'
    )
    font_family_small: str = (
        '"Segoe UI Variable Small", "Seoge UI Variable Static Small", var(--fds-font-family-fallback)'
    )
    font_family_display: str = (
        '"Segoe UI Variable Display", "Seoge UI Variable Static Display", var(--fds-font-family-fallback)'
    )


@dataclass
class FontSizes:
    caption_font_size: str = "12px"
    body_font_size: str = "14px"
    body_large_font_size: str = "18px"
    subtitle_font_size: str = "20px"
    title_font_size: str = "28px"
    title_large_font_size: str = "40px"
    display_font_size: str = "68px"


@dataclass
class Shadows:
    card_shadow: ft.BoxShadow = field(
        default_factory=lambda: ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.Colors.with_opacity(0.04, "#000000"),
            offset=ft.Offset(0, 2),
        )
    )

    tooltip_shadow: ft.BoxShadow = field(
        default_factory=lambda: ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.14, "#000000"),
            offset=ft.Offset(0, 4),
        )
    )

    flyout_shadow: ft.BoxShadow = field(
        default_factory=lambda: ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color=ft.Colors.with_opacity(0.14, "#000000"),
            offset=ft.Offset(0, 8),
        )
    )

    # For dialog_shadow we need multiple shadows, so we'll return a list
    @property
    def dialog_shadow(self) -> list[ft.BoxShadow]:
        return [
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=64,
                color=ft.Colors.with_opacity(0.1876, "#000000"),
                offset=ft.Offset(0, 32),
            ),
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=21,
                color=ft.Colors.with_opacity(0.1474, "#000000"),
                offset=ft.Offset(0, 2),
            ),
        ]

    # For inactive_window_shadow we need multiple shadows
    @property
    def inactive_window_shadow(self) -> list[ft.BoxShadow]:
        return [
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=32,
                color=ft.Colors.with_opacity(0.18, "#000000"),
                offset=ft.Offset(0, 16),
            ),
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=10.67,
                color=ft.Colors.with_opacity(0.1474, "#000000"),
                offset=ft.Offset(0, 2),
            ),
        ]

    # For active_window_shadow we need multiple shadows
    @property
    def active_window_shadow(self) -> list[ft.BoxShadow]:
        return [
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=64,
                color=ft.Colors.with_opacity(0.28, "#000000"),
                offset=ft.Offset(0, 32),
            ),
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=21,
                color=ft.Colors.with_opacity(0.22, "#000000"),
                offset=ft.Offset(0, 2),
            ),
        ]


@dataclass
class ControlFills:
    control_fill_transparent: str = "transparent"
    control_fill_default: str = None
    control_fill_secondary: str = None
    control_fill_tertiary: str = None
    control_fill_disabled: str = None
    control_fill_input_active: str = None
    control_strong_fill_default: str = None
    control_strong_fill_disabled: str = None
    control_solid_fill_default: str = None

    def get_fill(self, fill_name: str, override_opacity: float = None) -> str:
        fill_value = getattr(self, fill_name)
        if fill_value == "transparent":
            return ft.Colors.with_opacity(0, "#000000")
        if override_opacity is not None:
            return ft.Colors.with_opacity(override_opacity, fill_value)
        return fill_value


@dataclass
class LightControlFills(ControlFills):
    control_fill_default: str = ft.Colors.with_opacity(0.70, "#FFFFFF")
    control_fill_secondary: str = ft.Colors.with_opacity(0.50, "#FAFAFA")
    control_fill_tertiary: str = ft.Colors.with_opacity(0.30, "#FAFAFA")
    control_fill_disabled: str = ft.Colors.with_opacity(0.30, "#FAFAFA")
    control_fill_input_active: str = "#FFFFFF"
    control_strong_fill_default: str = ft.Colors.with_opacity(0.446, "#000000")
    control_strong_fill_disabled: str = ft.Colors.with_opacity(0.317, "#000000")
    control_solid_fill_default: str = "#FFFFFF"


@dataclass
class DarkControlFills(ControlFills):
    control_fill_default: str = ft.Colors.with_opacity(0.061, "#FFFFFF")
    control_fill_secondary: str = ft.Colors.with_opacity(0.084, "#FFFFFF")
    control_fill_tertiary: str = ft.Colors.with_opacity(0.033, "#FFFFFF")
    control_fill_disabled: str = ft.Colors.with_opacity(0.042, "#FFFFFF")
    control_fill_input_active: str = ft.Colors.with_opacity(0.70, "#1F1F1F")
    control_strong_fill_default: str = ft.Colors.with_opacity(0.544, "#FFFFFF")
    control_strong_fill_disabled: str = ft.Colors.with_opacity(0.247, "#FFFFFF")
    control_solid_fill_default: str = "#454545"


@dataclass
class BackgroundProperties:
    solid_background_base: str = None
    solid_background_secondary: str = None
    solid_background_tertiary: str = None
    solid_background_quarternary: str = None
    layer_background_default: str = None
    layer_background_alt: str = None
    card_background_default: str = None
    card_background_secondary: str = None
    smoke_background_default: str = None

    def get_background(
        self, background_name: str, override_opacity: float = None
    ) -> str:
        background_value = getattr(self, background_name)
        if override_opacity is not None:
            return ft.Colors.with_opacity(override_opacity, background_value)
        return background_value


@dataclass
class LightBackgrounds(BackgroundProperties):
    solid_background_base: str = "#F2F2F2"
    solid_background_secondary: str = "#EDEDED"
    solid_background_tertiary: str = "#FAFAFA"
    solid_background_quarternary: str = "#FFFFFF"
    layer_background_default: str = ft.Colors.with_opacity(0.50, "#FFFFFF")
    layer_background_alt: str = "#FFFFFF"
    card_background_default: str = ft.Colors.with_opacity(0.70, "#FFFFFF")
    card_background_secondary: str = ft.Colors.with_opacity(0.50, "#F5F5F5")
    smoke_background_default: str = ft.Colors.with_opacity(0.30, "#000000")


@dataclass
class DarkBackgrounds(BackgroundProperties):
    solid_background_base: str = "#212121"
    solid_background_secondary: str = "#1C1C1C"
    solid_background_tertiary: str = "#292929"
    solid_background_quarternary: str = "#2B2B2B"
    layer_background_default: str = ft.Colors.with_opacity(0.30, "#3A3A3A")
    layer_background_alt: str = ft.Colors.with_opacity(0.0538, "#FFFFFF")
    card_background_default: str = ft.Colors.with_opacity(0.0512, "#FFFFFF")
    card_background_secondary: str = ft.Colors.with_opacity(0.0326, "#FFFFFF")
    smoke_background_default: str = ft.Colors.with_opacity(0.30, "#000000")


@dataclass
class ThemeColors:
    text_primary: str = None
    text_secondary: str = None
    text_tertiary: str = None
    text_disabled: str = None
    accent_default: str = None
    accent_secondary: str = None
    accent_tertiary: str = None
    accent_disabled: str = None
    accent_text_primary: str = None
    accent_text_secondary: str = None
    accent_text_tertiary: str = None
    accent_text_disabled: str = None
    text_on_accent_primary: str = None
    text_on_accent_secondary: str = None
    text_on_accent_disabled: str = None
    text_on_accent_selected: str = None

    def get_color(self, color_name: str, override_opacity: float = None) -> str:
        color_value = getattr(self, color_name)
        if override_opacity is not None:
            return ft.Colors.with_opacity(override_opacity, color_value)
        return color_value


@dataclass
class LightThemeColors(ThemeColors):
    text_primary: str = ft.Colors.with_opacity(0.896, "#000000")
    text_secondary: str = ft.Colors.with_opacity(0.606, "#000000")
    text_tertiary: str = ft.Colors.with_opacity(0.446, "#000000")
    text_disabled: str = ft.Colors.with_opacity(0.361, "#000000")
    accent_default: str = "#005FB8"
    accent_secondary: str = ft.Colors.with_opacity(0.90, "#005FB8")
    accent_tertiary: str = ft.Colors.with_opacity(0.80, "#005FB8")
    accent_disabled: str = ft.Colors.with_opacity(0.217, "#000000")
    accent_text_primary: str = "#003A77"
    accent_text_secondary: str = "#002952"
    accent_text_tertiary: str = "#005FB8"
    accent_text_disabled: str = ft.Colors.with_opacity(0.361, "#000000")
    text_on_accent_primary: str = "#FFFFFF"
    text_on_accent_secondary: str = ft.Colors.with_opacity(0.70, "#FFFFFF")
    text_on_accent_disabled: str = ft.Colors.with_opacity(0.70, "#FFFFFF")
    text_on_accent_selected: str = "#FFFFFF"


@dataclass
class DarkThemeColors(ThemeColors):
    text_primary: str = "#FFFFFF"
    text_secondary: str = ft.Colors.with_opacity(0.786, "#FFFFFF")
    text_tertiary: str = ft.Colors.with_opacity(0.544, "#FFFFFF")
    text_disabled: str = ft.Colors.with_opacity(0.363, "#FFFFFF")
    accent_default: str = "#62B6F7"
    accent_secondary: str = ft.Colors.with_opacity(0.90, "#62B6F7")
    accent_tertiary: str = ft.Colors.with_opacity(0.80, "#62B6F7")
    accent_disabled: str = ft.Colors.with_opacity(0.158, "#FFFFFF")
    accent_text_primary: str = "#FFB4D9"
    accent_text_secondary: str = "#FFB4D9"
    accent_text_tertiary: str = "#62B6F7"
    accent_text_disabled: str = ft.Colors.with_opacity(0.363, "#FFFFFF")
    text_on_accent_primary: str = "#000000"
    text_on_accent_secondary: str = ft.Colors.with_opacity(0.50, "#000000")
    text_on_accent_disabled: str = ft.Colors.with_opacity(0.53, "#FFFFFF")
    text_on_accent_selected: str = "#FFFFFF"


@dataclass
class SystemColors:
    system_attention: str = "#005FB8"
    system_success: str = "#1F6621"
    system_caution: str = "#8C2800"
    system_critical: str = "#BC2F32"
    system_neutral: str = ft.Colors.with_opacity(0.446, "#000000")
    system_solid_neutral: str = "#8A8A8A"
    system_background_attention: str = ft.Colors.with_opacity(0.50, "#F5F5F5")
    system_background_success: str = "#E4F3E5"
    system_background_caution: str = "#FFECB3"
    system_background_critical: str = "#FEDED9"
    system_background_solid_attention: str = "#F7F7F7"
    system_background_solid_neutral: str = "#F2F2F2"

    def get_color(self, color_name: str, opacity: float = 1.0) -> str:
        color_value = getattr(self, color_name)
        if opacity != 1.0:
            return ft.Colors.with_opacity(opacity, color_value)
        return color_value


@dataclass
class Theme:
    colors: ThemeColors = None
    fills: ControlFills = None
    backgrounds: BackgroundProperties = None

    def get(self, property_name: str, opacity: float = None) -> str:
        # Try each category in order
        for category in [self.backgrounds, self.fills, self.colors]:
            if hasattr(category, property_name):
                if opacity is not None:
                    # Use the category's specific get method with opacity
                    if hasattr(category, "get_background"):
                        return category.get_background(property_name, opacity)
                    elif hasattr(category, "get_fill"):
                        return category.get_fill(property_name, opacity)
                    elif hasattr(category, "get_color"):
                        return category.get_color(property_name, opacity)
                return getattr(category, property_name)
        raise AttributeError(f"Property {property_name} not found in theme")

    def __getattr__(self, name: str):
        # Try each category in order
        for category in [self.backgrounds, self.fills, self.colors]:
            if hasattr(category, name):
                return getattr(category, name)
        raise AttributeError(f"Property {name} not found in theme")


@dataclass
class LightTheme(Theme):
    colors: ThemeColors = field(default_factory=LightThemeColors)
    fills: ControlFills = field(default_factory=LightControlFills)
    backgrounds: BackgroundProperties = field(default_factory=LightBackgrounds)


@dataclass
class DarkTheme(Theme):
    colors: ThemeColors = field(default_factory=DarkThemeColors)
    fills: ControlFills = field(default_factory=DarkControlFills)
    backgrounds: BackgroundProperties = field(default_factory=DarkBackgrounds)


@dataclass
class FluentDesignSystem:
    accent_colors: AccentColors = field(default_factory=AccentColors)
    font_families: FontFamilies = field(default_factory=FontFamilies)
    font_sizes: FontSizes = field(default_factory=FontSizes)
    control_properties: ControlProperties = field(default_factory=ControlProperties)
    light_theme: LightTheme = field(default_factory=LightTheme)
    dark_theme: DarkTheme = field(default_factory=DarkTheme)
    system_colors: SystemColors = field(default_factory=SystemColors)
    shadows: Shadows = field(default_factory=Shadows)
