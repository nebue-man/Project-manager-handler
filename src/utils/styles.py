"""
Visual styles and theme management for the Project Manager application.
Defines colors, fonts, and styling constants for a consistent look.
"""

import customtkinter as ctk

class AppColors:
    """Color scheme for the application."""

    # Primary Colors
    PRIMARY = "#2196F3"        # Blue
    PRIMARY_DARK = "#1976D2"   # Darker Blue
    PRIMARY_LIGHT = "#BBDEFB"  # Lighter Blue

    # Secondary Colors
    SECONDARY = "#FF9800"      # Amber/Orange
    SECONDARY_DARK = "#F57C00" # Darker Amber
    SECONDARY_LIGHT = "#FFE0B2" # Lighter Amber

    # Success Colors
    SUCCESS = "#4CAF50"        # Green
    SUCCESS_DARK = "#388E3C"   # Darker Green
    SUCCESS_LIGHT = "#C8E6C9"  # Lighter Green

    # Warning Colors
    WARNING = "#FF9800"        # Orange
    WARNING_DARK = "#F57C00"   # Darker Orange
    WARNING_LIGHT = "#FFE0B2"  # Lighter Orange

    # Error Colors
    ERROR = "#F44336"          # Red
    ERROR_DARK = "#D32F2F"     # Darker Red
    ERROR_LIGHT = "#FFCDD2"    # Lighter Red

    # Neutral Colors
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GRAY_50 = "#FAFAFA"
    GRAY_100 = "#F5F5F5"
    GRAY_200 = "#EEEEEE"
    GRAY_300 = "#E0E0E0"
    GRAY_400 = "#BDBDBD"
    GRAY_500 = "#9E9E9E"
    GRAY_600 = "#757575"
    GRAY_700 = "#616161"
    GRAY_800 = "#424242"
    GRAY_900 = "#212121"

    # Status Colors
    STATUS_PLANNING = "#2196F3"  # Blue
    STATUS_ACTIVE = "#8BC34A"     # Light Green
    STATUS_COMPLETED = "#607D8B" # Blue Gray
    STATUS_PAUSED = "#FF5722"     # Deep Orange

    # Priority Colors
    PRIORITY_LOW = "#4CAF50"     # Green
    PRIORITY_MEDIUM = "#FF9800"  # Orange
    PRIORITY_HIGH = "#F44336"    # Red

class AppFonts:
    """Font configurations for the application."""

    @staticmethod
    def get_font(size=12, weight="normal", family="Helvetica"):
        """Get a font with specified properties."""
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
    """Styling configuration for UI components."""

    # Card Styling
    CARD_CORNER_RADIUS = 12
    CARD_BORDER_WIDTH = 1
    CARD_BORDER_COLOR = AppColors.GRAY_300
    CARD_HOVER_BORDER_COLOR = AppColors.PRIMARY
    CARD_SHADOW_COLOR = AppColors.GRAY_400

    # Button Styling
    BUTTON_CORNER_RADIUS = 8
    BUTTON_BORDER_WIDTH = 0
    BUTTON_HEIGHT = 40
    BUTTON_PADDING = 20

    # Input Field Styling
    INPUT_CORNER_RADIUS = 8
    INPUT_BORDER_WIDTH = 1
    INPUT_BORDER_COLOR = AppColors.GRAY_300
    INPUT_FOCUS_BORDER_COLOR = AppColors.PRIMARY
    INPUT_HEIGHT = 35

    # Spacing Constants
    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 16
    SPACING_LG = 24
    SPACING_XL = 32
    SPACING_XXL = 48

    # Icon Sizes
    ICON_SM = 16
    ICON_MD = 24
    ICON_LG = 32
    ICON_XL = 48

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

class StyledFrame(ctk.CTkFrame):
    """A frame with modern styling."""

    def __init__(self, parent, **kwargs):
        # Set default styling
        default_style = {
            "corner_radius": AppStyles.CARD_CORNER_RADIUS,
            "border_width": AppStyles.CARD_BORDER_WIDTH,
            "fg_color": ("gray90", "gray20")  # Light/Dark mode
        }

        # Override defaults with provided kwargs
        default_style.update(kwargs)

        super().__init__(parent, **default_style)

class StyledButton(ctk.CTkButton):
    """A button with modern styling."""

    def __init__(self, parent, style="primary", **kwargs):
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

            super().__init__(parent, **style_config)

        except Exception as e:
            # Fallback to basic button if styling fails
            print(f"Warning: StyledButton creation failed: {e}")
            super().__init__(parent, **kwargs)

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