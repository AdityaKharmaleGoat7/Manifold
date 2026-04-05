"""
Animation package — importing this module auto-discovers all animators.
Each module uses @AnimationRegistry.register to self-register.
"""

from mathplt.core.registry import AnimationRegistry

AnimationRegistry.discover()
