"""
Interactive UI components with animations and hover effects.
Enhanced versions of standard UI components with smooth interactions.
"""

import customtkinter as ctk
from typing import Optional, Callable, Any
import sys
import os

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.styles import AppColors, AppFonts, AppStyles, StyledFrame, StyledButton
from utils.animations import animator, HoverEffects, AnimationType

class AnimatedButton(StyledButton):
    """Button with smooth hover and click animations."""

    def __init__(self, parent, pulse_on_click=False, hover_effect=True, **kwargs):
        self.pulse_on_click = pulse_on_click
        self.hover_effect = hover_effect
        self.original_color = kwargs.get('fg_color', AppColors.PRIMARY)

        try:
            super().__init__(parent, **kwargs)
            # Add hover effect
            if self.hover_effect:
                self._add_hover_effect()
        except Exception as e:
            print(f"Warning: AnimatedButton creation failed: {e}")
            super().__init__(parent, **kwargs)

    def _add_hover_effect(self):
        """Add hover animation effect."""
        def on_enter(event):
            try:
                hover_color = self._get_hover_color()
                animator.animate_color(
                    self, 'fg_color',
                    self.original_color,
                    hover_color,
                    duration=0.2,
                    easing=AnimationType.ease_out_quad
                )
            except:
                pass  # Fallback silently

        def on_leave(event):
            try:
                animator.animate_color(
                    self, 'fg_color',
                    self.cget('fg_color'),
                    self.original_color,
                    duration=0.2,
                    easing=AnimationType.ease_out_quad
                )
            except:
                pass  # Fallback silently

        def on_click(event):
            if self.pulse_on_click:
                try:
                    animator.pulse(self, duration=0.3, scale=1.05)
                except:
                    pass  # Fallback silently

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
        self.bind("<Button-1>", on_click)

    def _get_hover_color(self):
        """Get appropriate hover color based on button style."""
        current_color = self.original_color
        if isinstance(current_color, tuple):
            # Light/Dark theme colors
            if "primary" in str(current_color):
                return (AppColors.PRIMARY_DARK, AppColors.PRIMARY)
            elif "secondary" in str(current_color):
                return (AppColors.SECONDARY_DARK, AppColors.SECONDARY)
            elif "success" in str(current_color):
                return (AppColors.SUCCESS_DARK, AppColors.SUCCESS)
        else:
            # Single color
            if current_color == AppColors.PRIMARY:
                return AppColors.PRIMARY_DARK
            elif current_color == AppColors.SECONDARY:
                return AppColors.SECONDARY_DARK
            elif current_color == AppColors.SUCCESS:
                return AppColors.SUCCESS_DARK

        # Darken the color for hover effect
        try:
            return self._darken_color(current_color)
        except:
            return current_color

    def _darken_color(self, color: str) -> str:
        """Simple color darkening."""
        if color.startswith('#'):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            darker_rgb = tuple(max(0, c - 30) for c in rgb)
            return '#{:02x}{:02x}{:02x}'.format(*darker_rgb)
        return color

class AnimatedCard(StyledFrame):
    """Card with hover effects and smooth transitions."""

    def __init__(self, parent, hover_lift=True, hover_highlight=True, **kwargs):
        self.hover_lift = hover_lift
        self.hover_highlight = hover_highlight
        self.is_hovering = False

        # Enhanced default styling
        default_style = {
            "border_width": 1,
            "border_color": (AppColors.GRAY_200, AppColors.GRAY_700),
            "corner_radius": AppStyles.CARD_CORNER_RADIUS + 2,
            "fg_color": (AppColors.WHITE, AppColors.GRAY_800)
        }
        default_style.update(kwargs)

        super().__init__(parent, **default_style)

        # Add hover effects
        self._setup_hover_effects()

    def _setup_hover_effects(self):
        """Setup hover animations."""
        def on_enter(event):
            if not self.is_hovering:
                self.is_hovering = True
                try:
                    if self.hover_highlight:
                        # Highlight border
                        animator.animate_color(
                            self, 'border_color',
                            self.cget('border_color'),
                            AppColors.PRIMARY,
                            duration=0.2,
                            easing=AnimationType.ease_out_quad
                        )

                    if self.hover_lift:
                        # Simulate lift effect with subtle color change
                        animator.animate_color(
                            self, 'fg_color',
                            self.cget('fg_color'),
                            (AppColors.GRAY_50, AppColors.GRAY_750),
                            duration=0.2,
                            easing=AnimationType.ease_out_quad
                        )
                except:
                    pass  # Fallback silently

        def on_leave(event):
            if self.is_hovering:
                self.is_hovering = False
                try:
                    if self.hover_highlight:
                        # Restore border color
                        animator.animate_color(
                            self, 'border_color',
                            self.cget('border_color'),
                            (AppColors.GRAY_200, AppColors.GRAY_700),
                            duration=0.2,
                            easing=AnimationType.ease_out_quad
                        )

                    if self.hover_lift:
                        # Restore original color
                        animator.animate_color(
                            self, 'fg_color',
                            self.cget('fg_color'),
                            (AppColors.WHITE, AppColors.GRAY_800),
                            duration=0.2,
                            easing=AnimationType.ease_out_quad
                        )
                except:
                    pass  # Fallback silently

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)

class SmoothProgressBar(StyledFrame):
    """Smooth progress bar with animated transitions."""

    def __init__(self, parent, width=300, height=8, **kwargs):
        self.width = width
        self.height = height
        self.current_progress = 0
        self.target_progress = 0
        self.is_animating = False

        # Background frame
        super().__init__(
            parent,
            width=width,
            height=height,
            fg_color=(AppColors.GRAY_200, AppColors.GRAY_700),
            corner_radius=self.height // 2,
            **kwargs
        )

        # Progress fill frame
        self.progress_fill = StyledFrame(
            self,
            fg_color=AppColors.SUCCESS,
            corner_radius=self.height // 2
        )
        self.progress_fill.place(x=0, y=0, relwidth=0, relheight=1)

    def set_progress(self, value: float, animated=True):
        """
        Set progress value.

        Args:
            value: Progress value (0-100)
            animated: Whether to animate the change
        """
        value = max(0, min(100, value))  # Clamp to 0-100
        self.target_progress = value

        if animated and not self.is_animating:
            self._animate_progress()
        else:
            self._update_progress(self.target_progress)

    def _animate_progress(self):
        """Animate progress change."""
        if self.is_animating:
            return

        self.is_animating = True
        start_progress = self.current_progress

        def animate():
            duration = 0.5  # 500ms animation
            start_time = None

            def update():
                nonlocal start_time
                if start_time is None:
                    start_time = self.after(0, update)  # Get time on first call
                    return

                progress = (self.after_id - start_time) / (duration * 1000)  # Convert to seconds
                if progress >= 1.0:
                    self._update_progress(self.target_progress)
                    self.is_animating = False
                    return

                eased_progress = AnimationType.ease_out_cubic(min(1.0, max(0.0, progress)))
                current_value = start_progress + (self.target_progress - start_progress) * eased_progress
                self._update_progress(current_value)

                self.after(16, update)  # ~60 FPS

            update()

        animate()

    def _update_progress(self, value: float):
        """Update progress bar display."""
        self.current_progress = value
        rel_width = value / 100.0
        self.progress_fill.place(relwidth=rel_width)

        # Update color based on progress
        color = AppColors.get_progress_color(value)
        self.progress_fill.configure(fg_color=color)

    def get_progress(self) -> float:
        """Get current progress value."""
        return self.current_progress

class RippleButton(AnimatedButton):
    """Button with Material Design-style ripple effect."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.ripples = []

    def create_ripple(self, x, y):
        """Create a ripple effect at the given coordinates."""
        try:
            ripple = ctk.CTkFrame(
                self,
                fg_color="white",
                corner_radius=50,
                width=20,
                height=20
            )
            ripple.place(x=x, y=y)

            # Animate ripple expansion
            self._animate_ripple(ripple)

        except:
            pass  # Fallback silently

    def _animate_ripple(self, ripple):
        """Animate ripple expansion and fade."""
        def animate():
            try:
                # Expand ripple
                for i in range(10):
                    size = 20 + i * 8
                    ripple.configure(width=size, height=size)
                    # Adjust position to center
                    ripple.place_configure(
                        x=ripple.winfo_x() - 4,
                        y=ripple.winfo_y() - 4
                    )
                    self.after(20)

                # Remove ripple
                ripple.destroy()

            except:
                try:
                    ripple.destroy()
                except:
                    pass

        animate()

    def bind_click_with_ripple(self):
        """Bind click event with ripple effect."""
        def on_click(event):
            self.create_ripple(event.x, event.y)
            # Call original command if exists
            if self._command:
                self._command()

        # Store original command
        self._command = self.cget("command")
        self.configure(command=lambda: None)  # Temporarily disable
        self.bind("<Button-1>", on_click)

class LoadingSpinner(StyledFrame):
    """Animated loading spinner."""

    def __init__(self, parent, size=32, color=None, **kwargs):
        self.size = size
        self.color = color or AppColors.PRIMARY
        self.is_spinning = False
        self.angle = 0

        super().__init__(
            parent,
            width=size,
            height=size,
            fg_color="transparent",
            **kwargs
        )

        # Create spinner segments
        self.segments = []
        self._create_spinner()

    def _create_spinner(self):
        """Create spinner visual segments."""
        import math

        num_segments = 8
        for i in range(num_segments):
            angle = (360 / num_segments) * i

            # Calculate position
            x = self.size // 2 + (self.size // 3) * math.cos(math.radians(angle))
            y = self.size // 2 + (self.size // 3) * math.sin(math.radians(angle))

            segment = ctk.CTkFrame(
                self,
                width=4,
                height=4,
                fg_color=self.color,
                corner_radius=2
            )
            segment.place(x=x, y=y)
            self.segments.append(segment)

    def start(self):
        """Start spinner animation."""
        self.is_spinning = True
        self._animate_spin()

    def stop(self):
        """Stop spinner animation."""
        self.is_spinning = False

    def _animate_spin(self):
        """Animate spinning motion."""
        if not self.is_spinning:
            return

        self.angle = (self.angle + 15) % 360

        import math
        num_segments = len(self.segments)

        for i, segment in enumerate(self.segments):
            # Calculate new position
            base_angle = (360 / num_segments) * i + self.angle
            x = self.size // 2 + (self.size // 3) * math.cos(math.radians(base_angle))
            y = self.size // 2 + (self.size // 3) * math.sin(math.radians(base_angle))

            # Fade effect based on position
            fade = abs(math.sin(math.radians(base_angle)))
            segment.configure(fg_color=self._fade_color(self.color, fade))

            segment.place(x=x, y=y)

        self.after(50, self._animate_spin)

    def _fade_color(self, color: str, fade: float) -> str:
        """Apply fade effect to color."""
        if color.startswith('#'):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            bg_rgb = (255, 255, 255)  # Assume white background
            faded_rgb = tuple(int(bg_rgb[j] + (rgb[j] - bg_rgb[j]) * fade) for j in range(3))
            return '#{:02x}{:02x}{:02x}'.format(*faded_rgb)
        return color