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
    """Get color based on progress percentage."""
    if progress >= 80:
        return AppColors.SUCCESS
    elif progress >= 50:
        return AppColors.WARNING
    else:
        return AppColors.GRAY_500

def get_deadline_urgency_color(days_remaining):
    """Get color based on deadline urgency."""
    if days_remaining < 0:
        return AppColors.ERROR  # Overdue
    elif days_remaining == 0:
        return AppColors.ERROR  # Due today
    elif days_remaining <= 3:
        return AppColors.WARNING  # Soon
    elif days_remaining <= 7:
        return AppColors.PRIMARY  # Approaching
    else:
        return AppColors.SUCCESS  # Plenty of time

def apply_modern_theme():
    """Apply modern theme settings to CustomTkinter."""
    # Set appearance mode based on system preference initially
    ctk.set_appearance_mode("system")

    # Use modern color theme
    ctk.set_default_color_theme("blue")

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
    """A button with modern styling."""

    def __init__(self, parent, style="primary", **kwargs):
        if not CTK_AVAILABLE:
            # Mock button for testing
            self.parent = parent
            self.style = style
            self.kwargs = kwargs
            return

        try:
            # Define button styles
            styles = {
                "primary": {
                    "fg_color": (AppColors.PRIMARY, AppColors.PRIMARY_DARK),
                    "hover_color": (AppColors.PRIMARY_DARK, AppColors.PRIMARY),
                    "text_color": "white",
                    "corner_radius": AppStyles.BUTTON_CORNER_RADIUS,
                    "height": AppStyles.BUTTON_HEIGHT
                },
                "secondary": {
                    "fg_color": (AppColors.SECONDARY, AppColors.SECONDARY_DARK),
                    "hover_color": (AppColors.SECONDARY_DARK, AppColors.SECONDARY),
                    "text_color": "white",
                    "corner_radius": AppStyles.BUTTON_CORNER_RADIUS,
                    "height": AppStyles.BUTTON_HEIGHT
                },
                "success": {
                    "fg_color": (AppColors.SUCCESS, AppColors.SUCCESS_DARK),
                    "hover_color": (AppColors.SUCCESS_DARK, AppColors.SUCCESS),
                    "text_color": "white",
                    "corner_radius": AppStyles.BUTTON_CORNER_RADIUS,
                    "height": AppStyles.BUTTON_HEIGHT
                },
                "outline": {
                    "fg_color": "transparent",
                    "border_width": 2,
                    "border_color": AppColors.PRIMARY,
                    "text_color": (AppColors.PRIMARY, AppColors.PRIMARY_LIGHT),
                    "hover_color": (AppColors.GRAY_100, AppColors.GRAY_800),
                    "corner_radius": AppStyles.BUTTON_CORNER_RADIUS,
                    "height": AppStyles.BUTTON_HEIGHT
                },
                "ghost": {
                    "fg_color": "transparent",
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_300),
                    "hover_color": (AppColors.GRAY_100, AppColors.GRAY_800),
                    "corner_radius": AppStyles.BUTTON_CORNER_RADIUS,
                    "height": AppStyles.BUTTON_HEIGHT
                }
            }

            # Get the style configuration
            style_config = styles.get(style, styles["primary"])
            style_config.update(kwargs)

            self._button = ctk.CTkButton(parent, **style_config)

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
    """An entry field with modern styling."""

    def __init__(self, parent, **kwargs):
        try:
            default_style = {
                "corner_radius": AppStyles.INPUT_CORNER_RADIUS,
                "border_width": AppStyles.INPUT_BORDER_WIDTH,
                "border_color": AppColors.INPUT_BORDER_COLOR,
                "height": AppStyles.INPUT_HEIGHT,
                "font": AppFonts.get_font(12, "normal")
            }

            default_style.update(kwargs)
            super().__init__(parent, **default_style)

        except Exception as e:
            # Fallback to basic entry if styling fails
            print(f"Warning: StyledEntry creation failed: {e}")
            super().__init__(parent, **kwargs)

class StyledLabel(ctk.CTkLabel):
    """A label with modern styling options."""

    def __init__(self, parent, variant="body", **kwargs):
        try:
            variant_styles = {
                "title": {
                    "font": AppFonts.get_font(28, "bold"),
                    "text_color": (AppColors.GRAY_900, AppColors.WHITE)
                },
                "heading": {
                    "font": AppFonts.get_font(20, "bold"),
                    "text_color": (AppColors.GRAY_800, AppColors.GRAY_100)
                },
                "subheading": {
                    "font": AppFonts.get_font(16, "bold"),
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_200)
                },
                "body": {
                    "font": AppFonts.get_font(12, "normal"),
                    "text_color": (AppColors.GRAY_700, AppColors.GRAY_300)
                },
                "caption": {
                    "font": AppFonts.get_font(10, "normal"),
                    "text_color": (AppColors.GRAY_500, AppColors.GRAY_400)
                },
                "muted": {
                    "font": AppFonts.get_font(9, "normal"),
                    "text_color": (AppColors.GRAY_400, AppColors.GRAY_500)
                }
            }

            style_config = variant_styles.get(variant, variant_styles["body"])
            style_config.update(kwargs)

            super().__init__(parent, **style_config)

        except Exception as e:
            # Fallback to basic label if styling fails
            print(f"Warning: StyledLabel creation failed: {e}")
            super().__init__(parent, **kwargs)