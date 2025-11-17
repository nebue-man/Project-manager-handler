"""
Visual styles and theme management for the Project Manager application.
Defines colors, fonts, and styling constants for a consistent look.
"""

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    # Create a minimal mock for testing without the full GUI
    class MockCTkFont:
        def __init__(self, family="Helvetica", size=12, weight="normal"):
            self.family = family
            self.size = size
            self.weight = weight

    class ctk:
        @staticmethod
        def set_appearance_mode(mode):
            pass
        @staticmethod
        def set_default_color_theme(theme):
            pass
        class CTkFont:
            def __init__(self, **kwargs):
                pass
        class CTkFrame:
            def __init__(self, parent, **kwargs):
                pass
        class CTkButton:
            def __init__(self, parent, **kwargs):
                pass
        class CTkEntry:
            def __init__(self, parent, **kwargs):
                pass
        class CTkLabel:
            def __init__(self, parent, **kwargs):
                pass

class AppColors:
    """Modern color scheme for the application with enhanced visual appeal."""

    # Modern Primary Colors - Deeper, more sophisticated
    PRIMARY = "#1976D2"        # Deep Blue
    PRIMARY_DARK = "#1565C0"   # Darker Deep Blue
    PRIMARY_LIGHT = "#42A5F5"  # Light Deep Blue
    PRIMARY_ULTRA_LIGHT = "#E3F2FD"  # Very Light Blue

    # Modern Secondary Colors - Professional purple/indigo
    SECONDARY = "#673AB7"      # Deep Purple
    SECONDARY_DARK = "#512DA8" # Darker Deep Purple
    SECONDARY_LIGHT = "#9575CD" # Light Deep Purple
    SECONDARY_ULTRA_LIGHT = "#EDE7F6"  # Very Light Purple

    # Success Colors - Fresh green tones
    SUCCESS = "#2E7D32"        # Deep Green
    SUCCESS_DARK = "#1B5E20"   # Darker Deep Green
    SUCCESS_LIGHT = "#66BB6A"  # Light Deep Green
    SUCCESS_ULTRA_LIGHT = "#E8F5E8"  # Very Light Green

    # Warning Colors - Warm amber tones
    WARNING = "#F57C00"        # Deep Amber
    WARNING_DARK = "#EF6C00"   # Darker Deep Amber
    WARNING_LIGHT = "#FFB74D"  # Light Deep Amber
    WARNING_ULTRA_LIGHT = "#FFF3E0"  # Very Light Amber

    # Error Colors - Modern red
    ERROR = "#D32F2F"          # Deep Red
    ERROR_DARK = "#C62828"     # Darker Deep Red
    ERROR_LIGHT = "#EF5350"    # Light Deep Red
    ERROR_ULTRA_LIGHT = "#FFEBEE"  # Very Light Red

    # Neutral Colors - Refined gray scale
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GRAY_25 = "#FAFAFA"        # Very Light Gray
    GRAY_50 = "#F5F5F5"        # Extra Light Gray
    GRAY_100 = "#EEEEEE"       # Light Gray
    GRAY_200 = "#E0E0E0"       # Lighter Gray
    GRAY_300 = "#BDBDBD"       # Medium Light Gray
    GRAY_400 = "#9E9E9E"       # Medium Gray
    GRAY_500 = "#757575"       # Standard Gray
    GRAY_600 = "#616161"       # Medium Dark Gray
    GRAY_700 = "#424242"       # Dark Gray
    GRAY_800 = "#303030"       # Darker Gray
    GRAY_850 = "#212121"       # Very Dark Gray
    GRAY_900 = "#1A1A1A"       # Extra Dark Gray
    GRAY_950 = "#0D0D0D"       # Ultra Dark Gray

    # Modern Status Colors - More sophisticated palette
    STATUS_PLANNING = "#5C6BC0"     # Indigo
    STATUS_ACTIVE = "#26A69A"       # Teal
    STATUS_COMPLETED = "#78909C"    # Blue Gray
    STATUS_PAUSED = "#FF7043"       # Deep Orange
    STATUS_CANCELLED = "#8D6E63"    # Brown

    # Modern Priority Colors - Clear visual hierarchy
    PRIORITY_LOW = "#66BB6A"        # Light Green
    PRIORITY_MEDIUM = "#FFA726"     # Orange
    PRIORITY_HIGH = "#EF5350"       # Red
    PRIORITY_CRITICAL = "#E91E63"   # Pink

    # Accent Colors - For visual interest
    ACCENT_BLUE = "#039BE5"         # Light Blue
    ACCENT_GREEN = "#43A047"        # Green
    ACCENT_PURPLE = "#8E24AA"       # Purple
    ACCENT_ORANGE = "#FB8C00"       # Dark Orange
    ACCENT_TEAL = "#00897B"         # Teal
    ACCENT_CYAN = "#00ACC1"         # Cyan

    # Gradient Colors - For modern effects
    GRADIENT_PRIMARY = [PRIMARY, PRIMARY_LIGHT]
    GRADIENT_SECONDARY = [SECONDARY, SECONDARY_LIGHT]
    GRADIENT_SUCCESS = [SUCCESS, SUCCESS_LIGHT]
    GRADIENT_WARNING = [WARNING, WARNING_LIGHT]
    GRADIENT_ERROR = [ERROR, ERROR_LIGHT]

class AppFonts:
    """Font configurations for the application."""

    @staticmethod
    def get_font(size=12, weight="normal", family="Helvetica"):
        """Get a font with specified properties."""
        if not CTK_AVAILABLE:
            # Return mock font for testing
            return {"family": family, "size": size, "weight": weight}

        weight_map = {
            "normal": "normal",
            "bold": "bold",
            "light": "light"
        }

        try:
            return ctk.CTkFont(
                family=family,
                size=size,
                weight=weight_map.get(weight, "normal")
            )
        except Exception as e:
            # Fallback if font creation fails
            print(f"Warning: Font creation failed: {e}")
            return ("Helvetica", size, weight_map.get(weight, "normal"))

    # Predefined font styles (lazy initialization)
    @property
    def TITLE(self):
        return self.get_font(28, "bold")

    @property
    def HEADING(self):
        return self.get_font(20, "bold")

    @property
    def SUBHEADING(self):
        return self.get_font(16, "bold")

    @property
    def BODY(self):
        return self.get_font(12, "normal")

    @property
    def CAPTION(self):
        return self.get_font(10, "normal")

    @property
    def SMALL(self):
        return self.get_font(9, "normal")

# Create a global instance
app_fonts = AppFonts()

class AppStyles:
    """Modern styling configuration for enhanced visual appeal."""

    # Modern Card Styling - More sophisticated design
    CARD_CORNER_RADIUS = 16          # Softer corners
    CARD_BORDER_WIDTH = 1
    CARD_BORDER_COLOR = AppColors.GRAY_200
    CARD_HOVER_BORDER_COLOR = AppColors.PRIMARY
    CARD_SHADOW_COLOR = AppColors.GRAY_400
    CARD_HOVER_SHADOW_COLOR = AppColors.GRAY_600
    CARD_PADDING = 20                # More padding for modern look

    # Elevation levels for cards
    ELEVATION_NONE = 0
    ELEVATION_LOW = 2
    ELEVATION_MEDIUM = 4
    ELEVATION_HIGH = 8
    ELEVATION_HIGHEST = 16

    # Modern Button Styling - Professional and clean
    BUTTON_CORNER_RADIUS = 12        # Rounded but professional
    BUTTON_BORDER_WIDTH = 0
    BUTTON_HEIGHT = 44               # Taller for better touch targets
    BUTTON_PADDING_X = 24            # Horizontal padding
    BUTTON_PADDING_Y = 12            # Vertical padding
    BUTTON_FONT_SIZE = 14            # Modern font size
    BUTTON_TRANSITION_DURATION = 200 # ms

    # Modern Input Field Styling - Clean and accessible
    INPUT_CORNER_RADIUS = 10
    INPUT_BORDER_WIDTH = 2
    INPUT_BORDER_COLOR = AppColors.GRAY_200
    INPUT_FOCUS_BORDER_COLOR = AppColors.PRIMARY
    INPUT_ERROR_BORDER_COLOR = AppColors.ERROR
    INPUT_HEIGHT = 44                # Match button height
    INPUT_PADDING_X = 16
    INPUT_PADDING_Y = 12
    INPUT_FONT_SIZE = 14

    # Enhanced Spacing Constants - Better visual rhythm
    SPACING_XS = 4                  # 0.25rem
    SPACING_SM = 8                  # 0.5rem
    SPACING_MD = 16                 # 1rem
    SPACING_LG = 24                 # 1.5rem
    SPACING_XL = 32                 # 2rem
    SPACING_XXL = 48                # 3rem
    SPACING_XXXL = 64               # 4rem

    # Modern Icon Sizes - Better scalability
    ICON_XS = 12
    ICON_SM = 16
    ICON_MD = 20
    ICON_LG = 24
    ICON_XL = 32
    ICON_XXL = 48
    ICON_XXXL = 64

    # Typography Scale - Modern font sizes
    FONT_SIZE_XS = 10
    FONT_SIZE_SM = 12
    FONT_SIZE_BASE = 14
    FONT_SIZE_LG = 16
    FONT_SIZE_XL = 18
    FONT_SIZE_2XL = 24
    FONT_SIZE_3XL = 30
    FONT_SIZE_4XL = 36
    FONT_SIZE_5XL = 48

    # Line Heights - Better readability
    LINE_HEIGHT_TIGHT = 1.2
    LINE_HEIGHT_NORMAL = 1.4
    LINE_HEIGHT_RELAXED = 1.6
    LINE_HEIGHT_LOOSE = 1.8

    # Animation Durations - Smooth and professional
    ANIM_FAST = 150          # ms
    ANIM_NORMAL = 250        # ms
    ANIM_SLOW = 350          # ms
    ANIM_VERY_SLOW = 500     # ms

    # Border Widths - Consistent hierarchy
    BORDER_NONE = 0
    BORDER_THIN = 1
    BORDER_NORMAL = 2
    BORDER_THICK = 3
    BORDER_THICKER = 4

    # Opacity Levels - For subtle effects
    OPACITY_HIDDEN = 0.0
    OPACITY_FAINT = 0.1
    OPACITY_LIGHT = 0.3
    OPACITY_MEDIUM = 0.6
    OPACITY_STRONG = 0.8
    OPACITY_FULL = 1.0

    # Z-Index Layers - For proper stacking
    Z_BASE = 0
    Z_RAISED = 10
    Z_DROPDOWN = 1000
    Z_STICKY = 1020
    Z_FIXED = 1030
    Z_MODAL_BACKDROP = 1040
    Z_MODAL = 1050
    Z_POPOVER = 1060
    Z_TOOLTIP = 1070
    Z_TOAST = 1080

    # Border Radius Scale - Consistent rounding
    RADIUS_NONE = 0
    RADIUS_SM = 4
    RADIUS_BASE = 8
    RADIUS_MD = 12
    RADIUS_LG = 16
    RADIUS_XL = 20
    RADIUS_2XL = 24
    RADIUS_FULL = 9999

    # Component-Specific Styles
    SIDEBAR_WIDTH = 280          # Modern sidebar width
    SIDEBAR_COLLAPSED_WIDTH = 80
    HEADER_HEIGHT = 64           # Modern header height
    FOOTER_HEIGHT = 48           # Modern footer height

    # Breakpoints - For responsive design
    BREAKPOINT_SM = 640          # Small screens
    BREAKPOINT_MD = 768          # Medium screens
    BREAKPOINT_LG = 1024         # Large screens
    BREAKPOINT_XL = 1280         # Extra large screens
    BREAKPOINT_2XL = 1536        # 2X large screens

def get_progress_color(progress):
    """Get color based on progress percentage with enhanced visual feedback."""
    if progress >= 90:
        return AppColors.SUCCESS        # Excellent progress
    elif progress >= 75:
        return AppColors.SUCCESS_LIGHT  # Good progress
    elif progress >= 50:
        return AppColors.WARNING        # Moderate progress
    elif progress >= 25:
        return AppColors.WARNING_LIGHT  # Low progress
    else:
        return AppColors.GRAY_400       # Very low progress

def get_deadline_urgency_color(days_remaining):
    """Get color based on deadline urgency with granular feedback."""
    if days_remaining < 0:
        return AppColors.ERROR_DARK     # Overdue - critical
    elif days_remaining == 0:
        return AppColors.ERROR          # Due today - urgent
    elif days_remaining <= 1:
        return AppColors.ERROR_LIGHT    # Due tomorrow - very urgent
    elif days_remaining <= 3:
        return AppColors.WARNING_DARK   # Due this week - urgent
    elif days_remaining <= 7:
        return AppColors.WARNING        # Due next week - approaching
    elif days_remaining <= 14:
        return AppColors.ACCENT_ORANGE  # Due in two weeks - moderate
    elif days_remaining <= 30:
        return AppColors.ACCENT_BLUE    # Due this month - comfortable
    else:
        return AppColors.SUCCESS        # Plenty of time

def apply_modern_theme():
    """Apply modern theme settings to CustomTkinter."""
    if not CTK_AVAILABLE:
        return

    # Set appearance mode based on system preference initially
    ctk.set_appearance_mode("system")

    # Use modern color theme
    ctk.set_default_color_theme("blue")

# Enhanced Color and Visual Hierarchy Utilities
class ColorUtils:
    """Utilities for working with the enhanced color system."""

    @staticmethod
    def get_status_color(status: str) -> str:
        """Get color for project status."""
        status_colors = {
            "planning": AppColors.STATUS_PLANNING,
            "active": AppColors.STATUS_ACTIVE,
            "completed": AppColors.STATUS_COMPLETED,
            "paused": AppColors.STATUS_PAUSED,
            "cancelled": AppColors.STATUS_CANCELLED,
        }
        return status_colors.get(status.lower(), AppColors.GRAY_500)

    @staticmethod
    def get_priority_color(priority: str) -> str:
        """Get color for project priority."""
        priority_colors = {
            "low": AppColors.PRIORITY_LOW,
            "medium": AppColors.PRIORITY_MEDIUM,
            "high": AppColors.PRIORITY_HIGH,
            "critical": AppColors.PRIORITY_CRITICAL,
        }
        return priority_colors.get(priority.lower(), AppColors.GRAY_500)

    @staticmethod
    def create_gradient(start_color: str, end_color: str, steps: int = 10) -> list:
        """Create a gradient between two colors."""
        def hex_to_rgb(hex_color):
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*rgb)

        try:
            start_rgb = hex_to_rgb(start_color)
            end_rgb = hex_to_rgb(end_color)
            gradient = []

            for i in range(steps):
                t = i / (steps - 1) if steps > 1 else 0
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
                gradient.append(rgb_to_hex((r, g, b)))

            return gradient
        except:
            return [start_color, end_color]

    @staticmethod
    def get_contrast_color(bg_color: str) -> str:
        """Get a contrasting color for text on background."""
        def hex_to_rgb(hex_color):
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        try:
            rgb = hex_to_rgb(bg_color)
            # Calculate luminance
            luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
            return AppColors.BLACK if luminance > 0.5 else AppColors.WHITE
        except:
            return AppColors.BLACK

    @staticmethod
    def adjust_brightness(color: str, factor: float) -> str:
        """Adjust the brightness of a color."""
        def hex_to_rgb(hex_color):
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*rgb)

        try:
            rgb = hex_to_rgb(color)
            adjusted_rgb = tuple(max(0, min(255, int(c * factor))) for c in rgb)
            return rgb_to_hex(adjusted_rgb)
        except:
            return color

class VisualHierarchy:
    """Defines visual hierarchy rules for consistent UI design."""

    # Z-index layers for proper stacking
    LAYERS = {
        "background": AppStyles.Z_BASE,
        "content": AppStyles.Z_RAISED,
        "dropdown": AppStyles.Z_DROPDOWN,
        "sticky": AppStyles.Z_STICKY,
        "fixed": AppStyles.Z_FIXED,
        "modal_backdrop": AppStyles.Z_MODAL_BACKDROP,
        "modal": AppStyles.Z_MODAL,
        "popover": AppStyles.Z_POPOVER,
        "tooltip": AppStyles.Z_TOOLTIP,
        "toast": AppStyles.Z_TOAST,
    }

    # Typography hierarchy
    TYPOGRAPHY = {
        "display": {"variant": "h1", "size": "5xl", "weight": "bold"},
        "heading_1": {"variant": "h1", "size": "4xl", "weight": "bold"},
        "heading_2": {"variant": "h2", "size": "3xl", "weight": "bold"},
        "heading_3": {"variant": "h3", "size": "2xl", "weight": "bold"},
        "heading_4": {"variant": "h4", "size": "xl", "weight": "bold"},
        "heading_5": {"variant": "h5", "size": "lg", "weight": "bold"},
        "heading_6": {"variant": "h6", "size": "md", "weight": "bold"},
        "subtitle": {"variant": "subtitle", "size": "lg", "weight": "normal"},
        "body_large": {"variant": "body-large", "size": "lg", "weight": "normal"},
        "body": {"variant": "body", "size": "md", "weight": "normal"},
        "body_small": {"variant": "body-small", "size": "sm", "weight": "normal"},
        "caption": {"variant": "caption", "size": "sm", "weight": "normal"},
        "overline": {"variant": "overline", "size": "xs", "weight": "bold"},
        "label": {"variant": "body", "size": "sm", "weight": "medium"},
        "help": {"variant": "muted", "size": "xs", "weight": "normal"},
    }

    # Component visual hierarchy
    COMPONENTS = {
        "primary_action": {"style": "primary", "size": "md", "importance": "high"},
        "secondary_action": {"style": "secondary", "size": "md", "importance": "medium"},
        "tertiary_action": {"style": "outline", "size": "md", "importance": "low"},
        "danger_action": {"style": "error", "size": "md", "importance": "high"},
        "success_action": {"style": "success", "size": "md", "importance": "medium"},
        "fab": {"style": "fab", "size": "lg", "importance": "high"},
        "icon_button": {"style": "ghost", "size": "sm", "importance": "low"},
        "link": {"style": "link", "size": "md", "importance": "low"},
    }

    # Card elevation hierarchy
    ELEVATION = {
        "flat": AppStyles.ELEVATION_NONE,
        "low": AppStyles.ELEVATION_LOW,
        "medium": AppStyles.ELEVATION_MEDIUM,
        "high": AppStyles.ELEVATION_HIGH,
        "highest": AppStyles.ELEVATION_HIGHEST,
    }

    # Border radius hierarchy
    BORDER_RADIUS = {
        "none": AppStyles.RADIUS_NONE,
        "small": AppStyles.RADIUS_SM,
        "medium": AppStyles.RADIUS_BASE,
        "large": AppStyles.RADIUS_MD,
        "xl": AppStyles.RADIUS_LG,
        "2xl": AppStyles.RADIUS_XL,
        "3xl": AppStyles.RADIUS_2XL,
        "full": AppStyles.RADIUS_FULL,
    }

    # Spacing hierarchy
    SPACING = {
        "none": 0,
        "xs": AppStyles.SPACING_XS,
        "sm": AppStyles.SPACING_SM,
        "md": AppStyles.SPACING_MD,
        "lg": AppStyles.SPACING_LG,
        "xl": AppStyles.SPACING_XL,
        "2xl": AppStyles.SPACING_XXL,
        "3xl": AppStyles.SPACING_XXXL,
    }

    @staticmethod
    def get_layer_z_index(layer_name: str) -> int:
        """Get z-index for a layer name."""
        return VisualHierarchy.LAYERS.get(layer_name, AppStyles.Z_BASE)

    @staticmethod
    def get_typography_scale(text_type: str) -> dict:
        """Get typography configuration for text type."""
        return VisualHierarchy.TYPOGRAPHY.get(text_type, VisualHierarchy.TYPOGRAPHY["body"])

    @staticmethod
    def get_component_style(component_type: str) -> dict:
        """Get style configuration for component type."""
        return VisualHierarchy.COMPONENTS.get(component_type, VisualHierarchy.COMPONENTS["primary_action"])

    @staticmethod
    def get_elevation(elevation_level: str) -> int:
        """Get elevation value for level."""
        return VisualHierarchy.ELEVATION.get(elevation_level, AppStyles.ELEVATION_LOW)

    @staticmethod
    def get_border_radius(radius_size: str) -> int:
        """Get border radius value for size."""
        return VisualHierarchy.BORDER_RADIUS.get(radius_size, AppStyles.RADIUS_BASE)

    @staticmethod
    def get_spacing(spacing_size: str) -> int:
        """Get spacing value for size."""
        return VisualHierarchy.SPACING.get(spacing_size, AppStyles.SPACING_MD)

class ThemePresets:
    """Predefined theme combinations for consistent styling."""

    @staticmethod
    def get_project_card_colors(project_data: dict) -> dict:
        """Get color scheme for a project card based on its data."""
        priority = project_data.get("priority", "medium")
        status = project_data.get("status", "active")
        progress = project_data.get("progress", 0)

        colors = {
            "primary": ColorUtils.get_priority_color(priority),
            "secondary": ColorUtils.get_status_color(status),
            "progress": get_progress_color(progress),
            "text": (AppColors.GRAY_800, AppColors.GRAY_200),
            "muted": (AppColors.GRAY_500, AppColors.GRAY_400),
            "background": (AppColors.WHITE, AppColors.GRAY_850),
            "border": (AppColors.GRAY_200, AppColors.GRAY_700),
        }

        return colors

    @staticmethod
    def get_learning_card_colors(learning_data: dict) -> dict:
        """Get color scheme for a learning card."""
        tags = learning_data.get("tags", [])
        has_project = learning_data.get("project_id") is not None

        colors = {
            "primary": AppColors.ACCENT_PURPLE if has_project else AppColors.ACCENT_TEAL,
            "secondary": AppColors.SECONDARY if tags else AppColors.GRAY_400,
            "text": (AppColors.GRAY_800, AppColors.GRAY_200),
            "muted": (AppColors.GRAY_500, AppColors.GRAY_400),
            "background": (AppColors.WHITE, AppColors.GRAY_850),
            "border": (AppColors.GRAY_200, AppColors.GRAY_700),
        }

        return colors

    @staticmethod
    def get_sidebar_colors() -> dict:
        """Get color scheme for sidebar navigation."""
        return {
            "background": (AppColors.GRAY_50, AppColors.GRAY_900),
            "text": (AppColors.GRAY_700, AppColors.GRAY_300),
            "text_active": (AppColors.PRIMARY, AppColors.PRIMARY_LIGHT),
            "text_hover": (AppColors.GRAY_900, AppColors.GRAY_100),
            "border": (AppColors.GRAY_200, AppColors.GRAY_700),
            "accent": AppColors.PRIMARY,
            "success": AppColors.SUCCESS,
            "warning": AppColors.WARNING,
            "error": AppColors.ERROR,
        }

    @staticmethod
    def get_status_colors() -> dict:
        """Get comprehensive status color mapping."""
        return {
            "planning": {
                "bg": AppColors.STATUS_PLANNING,
                "text": AppColors.WHITE,
                "border": AppColors.PRIMARY_DARK,
            },
            "active": {
                "bg": AppColors.STATUS_ACTIVE,
                "text": AppColors.WHITE,
                "border": AppColors.SUCCESS_DARK,
            },
            "completed": {
                "bg": AppColors.STATUS_COMPLETED,
                "text": AppColors.WHITE,
                "border": AppColors.GRAY_700,
            },
            "paused": {
                "bg": AppColors.STATUS_PAUSED,
                "text": AppColors.WHITE,
                "border": AppColors.WARNING_DARK,
            },
            "cancelled": {
                "bg": AppColors.STATUS_CANCELLED,
                "text": AppColors.WHITE,
                "border": AppColors.GRAY_700,
            },
        }

# Create global instances for easy access
color_utils = ColorUtils()
visual_hierarchy = VisualHierarchy()
theme_presets = ThemePresets()

class StyledFrame:
    """A frame with modern styling."""

    def __init__(self, parent, **kwargs):
        if not CTK_AVAILABLE:
            # Mock frame for testing
            self.parent = parent
            self.kwargs = kwargs
            return

        try:
            # Set default styling
            default_style = {
                "corner_radius": AppStyles.CARD_CORNER_RADIUS,
                "border_width": AppStyles.CARD_BORDER_WIDTH,
                "fg_color": ("gray90", "gray20")  # Light/Dark mode
            }

            # Override defaults with provided kwargs
            default_style.update(kwargs)

            self._frame = ctk.CTkFrame(parent, **default_style)

        except Exception as e:
            # Fallback to basic frame if styling fails
            print(f"Warning: StyledFrame creation failed: {e}")
            try:
                self._frame = ctk.CTkFrame(parent, **kwargs)
            except:
                self._frame = None

    def __getattr__(self, name):
        """Delegate all other method calls to the actual frame."""
        if hasattr(self, '_frame') and self._frame:
            return getattr(self._frame, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

class StyledButton:
    """A button with enhanced modern styling and better visual feedback."""

    def __init__(self, parent, style="primary", size="md", **kwargs):
        if not CTK_AVAILABLE:
            # Mock button for testing
            self.parent = parent
            self.style = style
            self.size = size
            self.kwargs = kwargs
            return

        try:
            # Define size configurations
            sizes = {
                "xs": {
                    "height": 32,
                    "font": AppFonts.get_font(11, "normal"),
                    "corner_radius": 8
                },
                "sm": {
                    "height": 36,
                    "font": AppFonts.get_font(12, "normal"),
                    "corner_radius": 10
                },
                "md": {
                    "height": AppStyles.BUTTON_HEIGHT,
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "normal"),
                    "corner_radius": AppStyles.BUTTON_CORNER_RADIUS
                },
                "lg": {
                    "height": 48,
                    "font": AppFonts.get_font(16, "normal"),
                    "corner_radius": 14
                },
                "xl": {
                    "height": 56,
                    "font": AppFonts.get_font(18, "normal"),
                    "corner_radius": 16
                }
            }

            # Define enhanced button styles with modern colors
            styles = {
                "primary": {
                    "fg_color": (AppColors.PRIMARY, AppColors.PRIMARY_DARK),
                    "hover_color": (AppColors.PRIMARY_DARK, AppColors.PRIMARY),
                    "text_color": (AppColors.WHITE, AppColors.WHITE),
                    "border_color": (AppColors.PRIMARY, AppColors.PRIMARY_DARK),
                },
                "secondary": {
                    "fg_color": (AppColors.SECONDARY, AppColors.SECONDARY_DARK),
                    "hover_color": (AppColors.SECONDARY_DARK, AppColors.SECONDARY),
                    "text_color": (AppColors.WHITE, AppColors.WHITE),
                    "border_color": (AppColors.SECONDARY, AppColors.SECONDARY_DARK),
                },
                "success": {
                    "fg_color": (AppColors.SUCCESS, AppColors.SUCCESS_DARK),
                    "hover_color": (AppColors.SUCCESS_DARK, AppColors.SUCCESS),
                    "text_color": (AppColors.WHITE, AppColors.WHITE),
                    "border_color": (AppColors.SUCCESS, AppColors.SUCCESS_DARK),
                },
                "warning": {
                    "fg_color": (AppColors.WARNING, AppColors.WARNING_DARK),
                    "hover_color": (AppColors.WARNING_DARK, AppColors.WARNING),
                    "text_color": (AppColors.WHITE, AppColors.WHITE),
                    "border_color": (AppColors.WARNING, AppColors.WARNING_DARK),
                },
                "error": {
                    "fg_color": (AppColors.ERROR, AppColors.ERROR_DARK),
                    "hover_color": (AppColors.ERROR_DARK, AppColors.ERROR),
                    "text_color": (AppColors.WHITE, AppColors.WHITE),
                    "border_color": (AppColors.ERROR, AppColors.ERROR_DARK),
                },
                "outline": {
                    "fg_color": "transparent",
                    "border_width": AppStyles.BORDER_NORMAL,
                    "border_color": (AppColors.PRIMARY, AppColors.PRIMARY_LIGHT),
                    "text_color": (AppColors.PRIMARY, AppColors.PRIMARY_LIGHT),
                    "hover_color": (AppColors.PRIMARY_ULTRA_LIGHT, AppColors.GRAY_850),
                    "hover_border_color": (AppColors.PRIMARY_DARK, AppColors.PRIMARY),
                },
                "outline-secondary": {
                    "fg_color": "transparent",
                    "border_width": AppStyles.BORDER_NORMAL,
                    "border_color": (AppColors.GRAY_300, AppColors.GRAY_600),
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_300),
                    "hover_color": (AppColors.GRAY_100, AppColors.GRAY_800),
                    "hover_border_color": (AppColors.GRAY_500, AppColors.GRAY_400),
                },
                "ghost": {
                    "fg_color": "transparent",
                    "border_width": AppStyles.BORDER_NONE,
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_300),
                    "hover_color": (AppColors.GRAY_100, AppColors.GRAY_800),
                },
                "link": {
                    "fg_color": "transparent",
                    "border_width": AppStyles.BORDER_NONE,
                    "text_color": (AppColors.PRIMARY, AppColors.PRIMARY_LIGHT),
                    "hover_color": "transparent",
                    "hover_text_color": (AppColors.PRIMARY_DARK, AppColors.PRIMARY),
                    "font": AppFonts.get_font(14, "normal"),
                    "corner_radius": 4,
                },
                "fab": {  # Floating Action Button
                    "fg_color": (AppColors.SECONDARY, AppColors.SECONDARY_DARK),
                    "hover_color": (AppColors.SECONDARY_DARK, AppColors.SECONDARY),
                    "text_color": (AppColors.WHITE, AppColors.WHITE),
                    "corner_radius": 28,  # Circular
                    "width": 56,
                    "height": 56,
                }
            }

            # Get size configuration
            size_config = sizes.get(size, sizes["md"])

            # Get style configuration
            style_config = styles.get(style, styles["primary"])

            # Merge configurations, with kwargs having highest priority
            final_config = {**size_config, **style_config, **kwargs}

            self._button = ctk.CTkButton(parent, **final_config)

        except Exception as e:
            # Fallback to basic button if styling fails
            print(f"Warning: StyledButton creation failed: {e}")
            try:
                self._button = ctk.CTkButton(parent, **kwargs)
            except:
                self._button = None

    def __getattr__(self, name):
        """Delegate all other method calls to the actual button."""
        if hasattr(self, '_button') and self._button:
            return getattr(self._button, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

class StyledEntry(ctk.CTkEntry):
    """An entry field with enhanced modern styling and better UX."""

    def __init__(self, parent, variant="default", size="md", **kwargs):
        try:
            # Define size configurations
            sizes = {
                "sm": {
                    "height": 36,
                    "font": AppFonts.get_font(12, "normal"),
                    "corner_radius": 8
                },
                "md": {
                    "height": AppStyles.INPUT_HEIGHT,
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "normal"),
                    "corner_radius": AppStyles.INPUT_CORNER_RADIUS
                },
                "lg": {
                    "height": 52,
                    "font": AppFonts.get_font(16, "normal"),
                    "corner_radius": 12
                }
            }

            # Define variant configurations
            variants = {
                "default": {
                    "border_width": AppStyles.INPUT_BORDER_WIDTH,
                    "border_color": AppColors.INPUT_BORDER_COLOR,
                    "focus_border_color": AppColors.INPUT_FOCUS_BORDER_COLOR,
                    "text_color": (AppColors.GRAY_800, AppColors.GRAY_200),
                    "fg_color": (AppColors.WHITE, AppColors.GRAY_850),
                },
                "search": {
                    "border_width": AppStyles.BORDER_THIN,
                    "border_color": AppColors.GRAY_200,
                    "focus_border_color": AppColors.ACCENT_BLUE,
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_300),
                    "fg_color": (AppColors.GRAY_50, AppColors.GRAY_800),
                    "placeholder_text_color": (AppColors.GRAY_400, AppColors.GRAY_500),
                },
                "success": {
                    "border_width": AppStyles.BORDER_NORMAL,
                    "border_color": AppColors.SUCCESS_LIGHT,
                    "focus_border_color": AppColors.SUCCESS,
                    "text_color": (AppColors.SUCCESS_DARK, AppColors.SUCCESS_LIGHT),
                    "fg_color": (AppColors.SUCCESS_ULTRA_LIGHT, AppColors.GRAY_850),
                },
                "error": {
                    "border_width": AppStyles.BORDER_NORMAL,
                    "border_color": AppColors.ERROR_LIGHT,
                    "focus_border_color": AppColors.ERROR,
                    "text_color": (AppColors.ERROR_DARK, AppColors.ERROR_LIGHT),
                    "fg_color": (AppColors.ERROR_ULTRA_LIGHT, AppColors.GRAY_850),
                },
                "minimal": {
                    "border_width": AppStyles.BORDER_NONE,
                    "border_color": "transparent",
                    "focus_border_color": AppColors.PRIMARY,
                    "text_color": (AppColors.GRAY_800, AppColors.GRAY_200),
                    "fg_color": (AppColors.GRAY_100, AppColors.GRAY_850),
                }
            }

            # Get size and variant configurations
            size_config = sizes.get(size, sizes["md"])
            variant_config = variants.get(variant, variants["default"])

            # Merge configurations with kwargs having highest priority
            final_config = {**size_config, **variant_config, **kwargs}

            super().__init__(parent, **final_config)

        except Exception as e:
            # Fallback to basic entry if styling fails
            print(f"Warning: StyledEntry creation failed: {e}")
            super().__init__(parent, **kwargs)

class StyledLabel(ctk.CTkLabel):
    """A label with comprehensive modern styling options."""

    def __init__(self, parent, variant="body", size="md", **kwargs):
        try:
            # Define size configurations
            sizes = {
                "xs": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_XS, "normal")},
                "sm": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_SM, "normal")},
                "md": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "normal")},
                "lg": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_LG, "normal")},
                "xl": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_XL, "normal")},
                "2xl": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_2XL, "normal")},
                "3xl": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_3XL, "normal")},
                "4xl": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_4XL, "bold")},
                "5xl": {"font": AppFonts.get_font(AppStyles.FONT_SIZE_5XL, "bold")},
            }

            # Define variant configurations
            variants = {
                "hero": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_5XL, "bold"),
                    "text_color": (AppColors.GRAY_900, AppColors.WHITE),
                    "wraplength": 600,
                },
                "h1": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_4XL, "bold"),
                    "text_color": (AppColors.GRAY_900, AppColors.WHITE),
                },
                "h2": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_3XL, "bold"),
                    "text_color": (AppColors.GRAY_850, AppColors.GRAY_50),
                },
                "h3": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_2XL, "bold"),
                    "text_color": (AppColors.GRAY_800, AppColors.GRAY_100),
                },
                "h4": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_XL, "bold"),
                    "text_color": (AppColors.GRAY_800, AppColors.GRAY_100),
                },
                "h5": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_LG, "bold"),
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_200),
                },
                "h6": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "bold"),
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_200),
                },
                "subtitle": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_LG, "normal"),
                    "text_color": (AppColors.GRAY_600, AppColors.GRAY_400),
                    "wraplength": 400,
                },
                "body": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "normal"),
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_300),
                    "wraplength": 500,
                },
                "body-large": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_LG, "normal"),
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_300),
                    "wraplength": 600,
                },
                "body-small": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_SM, "normal"),
                    "text_color": (AppColors.GRAY_600, AppColors.GRAY_400),
                    "wraplength": 400,
                },
                "caption": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_SM, "normal"),
                    "text_color": (AppColors.GRAY_500, AppColors.GRAY_400),
                    "wraplength": 300,
                },
                "overline": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_XS, "bold"),
                    "text_color": (AppColors.GRAY_600, AppColors.GRAY_400),
                    "text_transform": "uppercase",
                    "letter_spacing": 1,
                },
                "muted": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_SM, "normal"),
                    "text_color": (AppColors.GRAY_400, AppColors.GRAY_500),
                    "opacity": 0.8,
                },
                "accent": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "bold"),
                    "text_color": (AppColors.PRIMARY, AppColors.PRIMARY_LIGHT),
                },
                "success": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "bold"),
                    "text_color": (AppColors.SUCCESS, AppColors.SUCCESS_LIGHT),
                },
                "warning": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "bold"),
                    "text_color": (AppColors.WARNING, AppColors.WARNING_LIGHT),
                },
                "error": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_BASE, "bold"),
                    "text_color": (AppColors.ERROR, AppColors.ERROR_LIGHT),
                },
                "code": {
                    "font": AppFonts.get_font(AppStyles.FONT_SIZE_SM, "normal", "Courier New"),
                    "text_color": (AppColors.ACCENT_PURPLE, AppColors.ACCENT_PURPLE),
                    "fg_color": (AppColors.GRAY_100, AppColors.GRAY_800),
                    "corner_radius": 4,
                    "padx": 8,
                    "pady": 4,
                },
            }

            # Get size and variant configurations
            size_config = sizes.get(size, {})
            variant_config = variants.get(variant, variants["body"])

            # Merge configurations with kwargs having highest priority
            final_config = {**size_config, **variant_config, **kwargs}

            super().__init__(parent, **final_config)

        except Exception as e:
            # Fallback to basic label if styling fails
            print(f"Warning: StyledLabel creation failed: {e}")
            super().__init__(parent, **kwargs)