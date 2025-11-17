"""
Animation utilities for smooth UI transitions and effects.
Provides functions for animating UI elements with different easing functions.
"""

import time
import threading
from typing import Callable, Optional, Any, Union, Tuple
import math

# Handle headless environment
try:
    import customtkinter as ctk
    GUI_AVAILABLE = True
except (ImportError, Exception):
    GUI_AVAILABLE = False
    # Mock for headless testing
    class MockCTk:
        def __init__(self):
            pass
        def after(self, *args, **kwargs): pass
        def configure(self, *args, **kwargs): pass
        def cget(self, *args): return None
        def winfo_width(self): return 100
        def winfo_height(self): return 40
        def set_opacity(self, opacity): pass
        def place(self, *args, **kwargs): pass
        def bind(self, *args, **kwargs): pass

    ctk = MockCTk()

class AnimationType:
    """Enhanced animation types with professional easing functions."""

    @staticmethod
    def linear(t: float) -> float:
        """Linear easing - constant speed."""
        return t

    # Quad Easing Functions
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease-in - accelerates from zero velocity."""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease-out - decelerates to zero velocity."""
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease-in-out - accelerates then decelerates."""
        if t < 0.5:
            return 2 * t * t
        return -1 + (4 - 2 * t) * t

    # Cubic Easing Functions
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease-in - smoother acceleration."""
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease-out - smoother deceleration."""
        p = t - 1
        return p * p * p + 1

    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease-in-out - very smooth acceleration/deceleration."""
        if t < 0.5:
            return 4 * t * t * t
        p = 2 * t - 2
        return 1 + p * p * p / 2

    # Quart Easing Functions
    @staticmethod
    def ease_in_quart(t: float) -> float:
        """Quartic ease-in - strong acceleration."""
        return t * t * t * t

    @staticmethod
    def ease_out_quart(t: float) -> float:
        """Quartic ease-out - strong deceleration."""
        p = t - 1
        return 1 - p * p * p * p

    @staticmethod
    def ease_in_out_quart(t: float) -> float:
        """Quartic ease-in-out - very strong acceleration/deceleration."""
        if t < 0.5:
            return 8 * t * t * t * t
        p = t - 1
        return 1 - 8 * p * p * p * p

    # Quint Easing Functions
    @staticmethod
    def ease_in_quint(t: float) -> float:
        """Quintic ease-in - very strong acceleration."""
        return t * t * t * t * t

    @staticmethod
    def ease_out_quint(t: float) -> float:
        """Quintic ease-out - very strong deceleration."""
        p = t - 1
        return 1 + p * p * p * p * p

    @staticmethod
    def ease_in_out_quint(t: float) -> float:
        """Quintic ease-in-out - extremely strong acceleration/deceleration."""
        if t < 0.5:
            return 16 * t * t * t * t * t
        p = (2 * t - 2)
        return 1 + 16 * p * p * p * p * p

    # Sine Easing Functions
    @staticmethod
    def ease_in_sine(t: float) -> float:
        """Sine ease-in - smooth, wave-like acceleration."""
        return 1 - math.cos((t * math.pi) / 2)

    @staticmethod
    def ease_out_sine(t: float) -> float:
        """Sine ease-out - smooth, wave-like deceleration."""
        return math.sin((t * math.pi) / 2)

    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        """Sine ease-in-out - smooth wave throughout."""
        return -(math.cos(math.pi * t) - 1) / 2

    # Exponential Easing Functions
    @staticmethod
    def ease_in_expo(t: float) -> float:
        """Exponential ease-in - slow start, then explosive acceleration."""
        return 0 if t == 0 else 2 ** (10 * t - 10)

    @staticmethod
    def ease_out_expo(t: float) -> float:
        """Exponential ease-out - explosive start, then smooth end."""
        return 1 if t == 1 else 1 - 2 ** (-10 * t)

    @staticmethod
    def ease_in_out_expo(t: float) -> float:
        """Exponential ease-in-out - very dynamic curve."""
        if t == 0:
            return 0
        if t == 1:
            return 1
        if t < 0.5:
            return 2 ** (20 * t - 10) / 2
        return (2 - 2 ** (-20 * t + 10)) / 2

    # Circular Easing Functions
    @staticmethod
    def ease_in_circ(t: float) -> float:
        """Circular ease-in - smooth circular acceleration."""
        return 1 - math.sqrt(1 - t * t)

    @staticmethod
    def ease_out_circ(t: float) -> float:
        """Circular ease-out - smooth circular deceleration."""
        p = t - 1
        return math.sqrt(1 - p * p)

    @staticmethod
    def ease_in_out_circ(t: float) -> float:
        """Circular ease-in-out - smooth circular motion."""
        if t < 0.5:
            return (1 - math.sqrt(1 - 4 * t * t)) / 2
        p = 2 * t - 2
        return (math.sqrt(1 - p * p) + 1) / 2

    # Back Easing Functions (Overshoot)
    @staticmethod
    def ease_in_back(t: float, overshoot: float = 1.70158) -> float:
        """Back ease-in - goes backwards before accelerating."""
        c1 = overshoot
        c3 = c1 + 1
        return c3 * t * t * t - c1 * t * t

    @staticmethod
    def ease_out_back(t: float, overshoot: float = 1.70158) -> float:
        """Back ease-out - overshoots then settles back."""
        c1 = overshoot
        c3 = c1 + 1
        return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

    @staticmethod
    def ease_in_out_back(t: float, overshoot: float = 1.70158) -> float:
        """Back ease-in-out - overshoots both ways."""
        c1 = overshoot * 1.525
        c2 = c1 + 1
        if t < 0.5:
            return ((2 * t) ** 2 * ((c2 + 1) * 2 * t - c2)) / 2
        return ((2 * t - 2) ** 2 * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

    # Elastic Easing Functions
    @staticmethod
    def ease_in_elastic(t: float, amplitude: float = 1.0, period: float = 0.5) -> float:
        """Elastic ease-in - bouncy acceleration."""
        if t == 0 or t == 1:
            return t
        c4 = (2 * math.pi) / period
        return -(amplitude * 2 ** (10 * t - 10)) * math.sin((t * 10 - 10.75) * c4)

    @staticmethod
    def ease_out_elastic(t: float, amplitude: float = 1.0, period: float = 0.5) -> float:
        """Elastic ease-out - bouncy deceleration."""
        if t == 0 or t == 1:
            return t
        c4 = (2 * math.pi) / period
        return amplitude * 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * c4) + 1

    @staticmethod
    def ease_in_out_elastic(t: float, amplitude: float = 1.0, period: float = 0.5) -> float:
        """Elastic ease-in-out - bouncy throughout."""
        if t == 0 or t == 1:
            return t
        c5 = (2 * math.pi) / (period * 1.5)
        if t < 0.5:
            return -(amplitude * 2 ** (20 * t - 10) * math.sin((20 * t - 11.125) * c5)) / 2
        return (amplitude * 2 ** (-20 * t + 10) * math.sin((20 * t - 11.125) * c5)) / 2 + 1

    # Bounce Easing Functions
    @staticmethod
    def ease_in_bounce(t: float) -> float:
        """Bounce ease-in - bouncing into position."""
        return 1 - AnimationType.ease_out_bounce(1 - t)

    @staticmethod
    def ease_out_bounce(t: float) -> float:
        """Bounce ease-out - bouncing out of position."""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            p = t - 1.5 / 2.75
            return 7.5625 * p * p + 0.75
        elif t < 2.5 / 2.75:
            p = t - 2.25 / 2.75
            return 7.5625 * p * p + 0.9375
        else:
            p = t - 2.625 / 2.75
            return 7.5625 * p * p + 0.984375

    @staticmethod
    def ease_in_out_bounce(t: float) -> float:
        """Bounce ease-in-out - bouncing both ways."""
        if t < 0.5:
            return (1 - AnimationType.ease_out_bounce(1 - 2 * t)) / 2
        return (1 + AnimationType.ease_out_bounce(2 * t - 1)) / 2

    # Custom Presets
    @staticmethod
    def smooth(t: float) -> float:
        """Smooth transition - perfect for most UI animations."""
        return AnimationType.ease_in_out_cubic(t)

    @staticmethod
    def snappy(t: float) -> float:
        """Snappy transition - quick with slight overshoot."""
        return AnimationType.ease_out_back(t, 1.2)

    @staticmethod
    def bouncy(t: float) -> float:
        """Bouncy transition - playful and engaging."""
        return AnimationType.ease_out_elastic(t, 0.8, 0.4)

    @staticmethod
    def dramatic(t: float) -> float:
        """Dramatic transition - strong acceleration."""
        return AnimationType.ease_in_out_expo(t)

class UIAnimator:
    """Handles UI animations with smooth transitions."""

    def __init__(self):
        """Initialize animator."""
        self.animations = []
        self.is_running = True

    def animate_color(self, widget, property_name: str, start_color: str,
                      end_color: str, duration: float = 0.3,
                      easing: Callable = AnimationType.ease_out_quad,
                      callback: Optional[Callable] = None):
        """
        Animate a color property of a widget.

        Args:
            widget: Widget to animate
            property_name: Property to animate (e.g., 'fg_color', 'border_color')
            start_color: Starting color
            end_color: Ending color
            duration: Animation duration in seconds
            easing: Easing function
            callback: Optional callback when animation completes
        """
        def animate():
            start_time = time.time()
            end_time = start_time + duration

            def update():
                current_time = time.time()
                if current_time >= end_time:
                    # Animation complete
                    widget.configure(**{property_name: end_color})
                    if callback:
                        callback()
                    return

                progress = (current_time - start_time) / duration
                eased_progress = easing(min(1.0, max(0.0, progress)))

                # Interpolate colors
                current_color = self._interpolate_color(start_color, end_color, eased_progress)
                widget.configure(**{property_name: current_color})

                if self.is_running:
                    widget.after(16, update)  # ~60 FPS

            update()

        # Run in separate thread to avoid blocking
        threading.Thread(target=animate, daemon=True).start()

    def animate_size(self, widget, start_size: tuple, end_size: tuple,
                     duration: float = 0.3, easing: Callable = AnimationType.ease_out_quad,
                     callback: Optional[Callable] = None):
        """
        Animate widget size.

        Args:
            widget: Widget to animate
            start_size: Starting (width, height)
            end_size: Ending (width, height)
            duration: Animation duration
            easing: Easing function
            callback: Optional callback
        """
        def animate():
            start_time = time.time()
            end_time = start_time + duration

            def update():
                current_time = time.time()
                if current_time >= end_time:
                    # Animation complete
                    widget.configure(width=end_size[0], height=end_size[1])
                    if callback:
                        callback()
                    return

                progress = (current_time - start_time) / duration
                eased_progress = easing(min(1.0, max(0.0, progress)))

                current_width = start_size[0] + (end_size[0] - start_size[0]) * eased_progress
                current_height = start_size[1] + (end_size[1] - start_size[1]) * eased_progress

                widget.configure(width=current_width, height=current_height)

                if self.is_running:
                    widget.after(16, update)

            update()

        threading.Thread(target=animate, daemon=True).start()

    def fade_in(self, widget, duration: float = 0.3,
                easing: Callable = AnimationType.ease_out_quad,
                callback: Optional[Callable] = None):
        """Fade in a widget by animating its alpha."""
        # This is a simplified fade effect using opacity
        start_alpha = 0.0
        end_alpha = 1.0

        def animate():
            start_time = time.time()
            end_time = start_time + duration

            def update():
                current_time = time.time()
                if current_time >= end_time:
                    # Animation complete
                    widget.set_opacity(1.0)
                    if callback:
                        callback()
                    return

                progress = (current_time - start_time) / duration
                eased_progress = easing(min(1.0, max(0.0, progress)))

                current_alpha = start_alpha + (end_alpha - start_alpha) * eased_progress
                widget.set_opacity(current_alpha)

                if self.is_running:
                    widget.after(16, update)

            update()

        threading.Thread(target=animate, daemon=True).start()

    def slide_in(self, widget, direction: str = "right", distance: int = 100,
                 duration: float = 0.3, easing: Callable = AnimationType.ease_out_quad,
                 callback: Optional[Callable] = None):
        """
        Slide in a widget from a direction.

        Args:
            widget: Widget to animate
            direction: "left", "right", "up", or "down"
            distance: Distance to slide from
            duration: Animation duration
            easing: Easing function
            callback: Optional callback
        """
        start_x, start_y = 0, 0
        end_x, end_y = 0, 0

        if direction == "left":
            start_x = -distance
        elif direction == "right":
            start_x = distance
        elif direction == "up":
            start_y = -distance
        elif direction == "down":
            start_y = distance

        def animate():
            start_time = time.time()
            end_time = start_time + duration

            def update():
                current_time = time.time()
                if current_time >= end_time:
                    # Animation complete
                    widget.place(relx=0.5, rely=0.5, anchor="center", x=end_x, y=end_y)
                    if callback:
                        callback()
                    return

                progress = (current_time - start_time) / duration
                eased_progress = easing(min(1.0, max(0.0, progress)))

                current_x = start_x + (end_x - start_x) * eased_progress
                current_y = start_y + (end_y - start_y) * eased_progress

                widget.place(relx=0.5, rely=0.5, anchor="center", x=current_x, y=current_y)

                if self.is_running:
                    widget.after(16, update)

            update()

        threading.Thread(target=animate, daemon=True).start()

    def pulse(self, widget, duration: float = 0.5, scale: float = 1.05,
              easing: Callable = AnimationType.ease_in_out_quad,
              callback: Optional[Callable] = None):
        """
        Pulse a widget (scale up and down).

        Args:
            widget: Widget to animate
            duration: Animation duration
            scale: Scale factor
            easing: Easing function
            callback: Optional callback
        """
        def animate():
            start_time = time.time()
            end_time = start_time + duration

            # Get original size
            original_width = widget.winfo_width()
            original_height = widget.winfo_height()

            def update():
                current_time = time.time()
                if current_time >= end_time:
                    # Animation complete - return to original size
                    widget.configure(width=original_width, height=original_height)
                    if callback:
                        callback()
                    return

                progress = (current_time - start_time) / duration
                eased_progress = easing(min(1.0, max(0.0, progress)))

                # Create pulse effect
                if progress < 0.5:
                    # Scale up
                    pulse_progress = progress * 2
                    current_scale = 1.0 + (scale - 1.0) * pulse_progress
                else:
                    # Scale down
                    pulse_progress = (progress - 0.5) * 2
                    current_scale = scale - (scale - 1.0) * pulse_progress

                current_width = original_width * current_scale
                current_height = original_height * current_scale

                widget.configure(width=current_width, height=current_height)

                if self.is_running:
                    widget.after(16, update)

            update()

        threading.Thread(target=animate, daemon=True).start()

    def _interpolate_color(self, color1: str, color2: str, t: float) -> str:
        """
        Interpolate between two colors.

        Args:
            color1: Starting color (hex or name)
            color2: Ending color (hex or name)
            t: Interpolation factor (0.0 to 1.0)

        Returns:
            Interpolated color in hex format
        """
        # Convert colors to RGB
        def hex_to_rgb(hex_color):
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*rgb)

        try:
            rgb1 = hex_to_rgb(color1) if color1.startswith('#') else (50, 50, 50)
            rgb2 = hex_to_rgb(color2) if color2.startswith('#') else (200, 200, 200)

            # Interpolate each channel
            r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * t)
            g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * t)
            b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * t)

            return rgb_to_hex((r, g, b))
        except:
            return color2  # Fallback to end color

    def stop_all(self):
        """Stop all running animations."""
        self.is_running = False

class HoverEffects:
    """Provides hover effects for widgets."""

    @staticmethod
    def add_hover_effect(widget, hover_color: str = None, hover_scale: float = None,
                        duration: float = 0.2):
        """
        Add hover effect to a widget.

        Args:
            widget: Widget to add effect to
            hover_color: Color to change to on hover
            hover_scale: Scale factor on hover
            duration: Animation duration
        """
        original_color = None
        original_size = None

        def on_enter(event):
            nonlocal original_color, original_size

            if hover_color:
                original_color = widget.cget("fg_color")
                widget.configure(fg_color=hover_color)

            if hover_scale:
                original_size = (widget.winfo_width(), widget.winfo_height())
                new_width = original_size[0] * hover_scale
                new_height = original_size[1] * hover_scale
                widget.configure(width=new_width, height=new_height)

        def on_leave(event):
            if original_color:
                widget.configure(fg_color=original_color)

            if original_size:
                widget.configure(width=original_size[0], height=original_size[1])

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

# Global animator instance
animator = UIAnimator()