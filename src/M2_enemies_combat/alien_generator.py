"""Procedural Alien Geometry Generator: Crystalline Void Invaders."""
import math
from OpenGL.GL import *
from OpenGL.GLUT import *


class AlienGenerator:
    """
    Procedural Crystalline Void Alien Generator:
    Constructs otherworldly dimensional invaders from faceted obsidian shards,
    glowing cyan/violet rift fissure cores, and rotating orbital matrices.
    """

    @staticmethod
    def draw_stalker(anim_time: float):
        """
        Rift Stalker: Predatory quadrupedal crystalline shadow-hound with
        articulated scythe blades and glowing rift fissure nodes.
        """
        glPushMatrix()

        # Run cycle animation parameters
        stride = math.sin(anim_time * 8.0)
        leg_rot = stride * 30.0
        blade_swing = math.sin(anim_time * 8.0 + 1.5) * 25.0

        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives

        # 1. Main Obsidian Carapace (Spine & Ribs)
        Materials.bind_alien_carapace()
        glColor3f(0.85, 0.75, 0.95)
        glPushMatrix()
        glTranslatef(0.0, 0.9, 0.0)
        glScalef(0.6, 0.45, 1.2)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()
        Materials.unbind_all()

        # 2. Glowing Cyan/Violet Rift Fissure Core (Inside Chest)
        pulse = 1.0 + 0.15 * math.sin(anim_time * 10.0)
        glColor3f(0.0, 0.85 * pulse, 1.0)
        glPushMatrix()
        glTranslatef(0.0, 0.9, 0.1)
        glScalef(0.35 * pulse, 0.35 * pulse, 0.5 * pulse)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()

        # 3. Predatory Angular Head
        glPushMatrix()
        glTranslatef(0.0, 1.0, 0.85)
        glRotatef(12.0, 1.0, 0.0, 0.0)
        Materials.bind_alien_carapace()
        glColor3f(0.9, 0.8, 1.0)
        glPushMatrix()
        glScalef(0.4, 0.3, 0.55)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()
        Materials.unbind_all()

        # 4 Glowing Cyan Sensory Eyes
        glColor3f(0.0, 1.0, 0.9)
        for dx, dy, dz in [(-0.14, 0.08, 0.2), (0.14, 0.08, 0.2), (-0.08, -0.05, 0.26), (0.08, -0.05, 0.26)]:
            glPushMatrix()
            glTranslatef(dx, dy, dz)
            glutSolidSphere(0.05, 6, 6)
            glPopMatrix()
        glPopMatrix()

        # 4. Front Articulated Scythe/Blade Arms
        glColor3f(0.2, 0.15, 0.3)
        for side in (-1, 1):
            glPushMatrix()
            glTranslatef(side * 0.45, 1.0, 0.4)
            glRotatef(side * 20.0, 0.0, 1.0, 0.0)
            glRotatef(blade_swing * side, 1.0, 0.0, 0.0)

            # Upper blade arm
            glPushMatrix()
            glRotatef(side * -25.0, 0.0, 0.0, 1.0)
            glTranslatef(side * 0.2, -0.2, 0.1)
            glScalef(0.12, 0.45, 0.12)
            Primitives.draw_textured_cube(1.0)
            glPopMatrix()

            # Razor-Sharp Crystalline Scythe Blade
            glColor3f(0.0, 0.9, 1.0)
            glPushMatrix()
            glTranslatef(side * 0.35, -0.45, 0.35)
            glRotatef(45.0, 1.0, 0.0, 0.0)
            glScalef(0.08, 0.6, 0.25)
            Primitives.draw_textured_octahedron(1.0)
            glPopMatrix()
            glColor3f(0.2, 0.15, 0.3)

            glPopMatrix()

        # 5. Quadrupedal Crystalline Legs (Back & Front Legs)
        for side in (-1, 1):
            for i, z_pos in enumerate([-0.35, 0.25]):
                sign = 1 if i == 0 else -1
                swing = leg_rot * sign * side
                glPushMatrix()
                glTranslatef(side * 0.45, 0.8, z_pos)
                glRotatef(side * 30.0, 0.0, 1.0, 0.0)
                glRotatef(swing, 1.0, 0.0, 0.0)

                # Upper Leg
                glPushMatrix()
                glRotatef(side * -25.0, 0.0, 0.0, 1.0)
                glTranslatef(side * 0.2, -0.25, 0.0)
                glScalef(0.14, 0.5, 0.14)
                Primitives.draw_textured_cube(1.0)
                glPopMatrix()

                # Lower Taloned Leg
                glPushMatrix()
                glTranslatef(side * 0.35, -0.55, 0.0)
                glRotatef(side * 40.0, 0.0, 0.0, 1.0)
                glScalef(0.1, 0.6, 0.1)
                Primitives.draw_textured_cube(1.0)
                glPopMatrix()

                glPopMatrix()

        glPopMatrix()

    @staticmethod
    def draw_spitter(anim_time: float):
        """
        Rift Spitter: Floating dimensional crystal monolith / prism
        surrounded by concentric orbital rotating shard rings.
        """
        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives

        glPushMatrix()
        hover = math.sin(anim_time * 3.0) * 0.2
        glTranslatef(0.0, 1.8 + hover, 0.0)

        # 1. Central Hovering Faceted Obsidian Monolith
        pulse = 1.0 + 0.1 * math.sin(anim_time * 5.0)
        Materials.bind_alien_carapace()
        glColor3f(0.9, 0.8, 1.0)
        glPushMatrix()
        glRotatef(anim_time * 30.0, 0.0, 1.0, 0.0)
        glScalef(0.65 * pulse, 1.5 * pulse, 0.65 * pulse)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()
        Materials.unbind_all()

        # 2. Glowing Plasma Energy Eye (Charging Core)
        glColor3f(0.0, 1.0, 0.65)
        glPushMatrix()
        glTranslatef(0.0, 0.2, 0.55)
        glScalef(0.25, 0.25, 0.35)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()

        # 3. Inner Orbital Rotating Shard Ring
        rot_inner = anim_time * 90.0
        glColor3f(0.8, 0.6, 1.0)
        glPushMatrix()
        glRotatef(rot_inner, 0.0, 1.0, 0.0)
        glRotatef(25.0, 1.0, 0.0, 0.0)
        for i in range(4):
            glPushMatrix()
            glRotatef(i * 90.0, 0.0, 1.0, 0.0)
            glTranslatef(1.25, 0.0, 0.0)
            glScalef(0.2, 0.45, 0.2)
            Primitives.draw_textured_octahedron(1.0)
            glPopMatrix()
        glPopMatrix()

        # 4. Outer Counter-Rotating Shard Ring with Glowing Nodes
        rot_outer = anim_time * -65.0
        glPushMatrix()
        glRotatef(rot_outer, 0.0, 1.0, 0.0)
        glRotatef(-35.0, 1.0, 0.0, 0.0)
        for i in range(6):
            glPushMatrix()
            glRotatef(i * 60.0, 0.0, 1.0, 0.0)
            glTranslatef(1.8, 0.0, 0.0)
            glColor3f(0.0, 0.85, 1.0)
            glScalef(0.18, 0.35, 0.18)
            glutSolidOctahedron()
            glPopMatrix()
        glPopMatrix()

        # 5. Glowing Energy Halo
        glColor4f(0.0, 1.0, 0.8, 0.6)
        glPushMatrix()
        glRotatef(anim_time * 120.0, 0.0, 1.0, 0.0)
        glutSolidTorus(0.04, 1.45, 8, 16)
        glPopMatrix()

        glPopMatrix()

    @staticmethod
    def draw_guardian_boss(anim_time: float, phase: int = 1):
        """
        Rift Guardian: Colossal dimensional nexus entity featuring a massive
        pulsating central obsidian polyhedron core and 4 orbiting shield obelisks.
        """
        glPushMatrix()
        hover = math.sin(anim_time * 2.0) * 0.3
        glTranslatef(0.0, 3.8 + hover, 0.0)

        # 1. Central Pulsating Nexus Polyhedron Core
        pulse_rate = 4.0 if phase == 1 else 8.0
        pulse = 1.0 + 0.08 * math.sin(anim_time * pulse_rate)

        from src.M4_rendering_gameplay.materials import Materials
        from src.M4_rendering_gameplay.primitives import Primitives

        # Inner Glowing Energy Heart
        glColor3f(1.0, 0.1, 0.35)
        glPushMatrix()
        glRotatef(anim_time * 50.0, 0.0, 1.0, 0.0)
        glScalef(1.4 * pulse, 2.0 * pulse, 1.4 * pulse)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()

        # Outer Obsidian Crystal Lattice
        Materials.bind_alien_carapace()
        glColor3f(0.9, 0.8, 1.0)
        glPushMatrix()
        glRotatef(anim_time * -35.0, 0.0, 1.0, 0.0)
        glScalef(1.9 * pulse, 2.5 * pulse, 1.9 * pulse)
        Primitives.draw_textured_octahedron(1.0)
        glPopMatrix()
        Materials.unbind_all()

        # 2. Four Independent Orbiting Defensive Shield Obelisks
        shield_speed = 50.0 if phase == 1 else 135.0
        shield_dist = 3.5 if phase == 1 else 4.6
        rot_shield = anim_time * shield_speed

        for i in range(4):
            glPushMatrix()
            glRotatef(rot_shield + i * 90.0, 0.0, 1.0, 0.0)
            glTranslatef(shield_dist, 0.0, 0.0)

            # Shield Obelisk Body
            Materials.bind_alien_carapace()
            glColor3f(0.85, 0.75, 0.95)
            glPushMatrix()
            glScalef(0.4, 2.2, 1.1)
            Primitives.draw_textured_cube(1.0)
            glPopMatrix()
            Materials.unbind_all()

            # Glowing Rift Rune Stripe on Shield Face
            rune_color = (0.0, 0.9, 1.0) if phase == 1 else (1.0, 0.2, 0.1)
            glColor3f(*rune_color)
            glPushMatrix()
            glTranslatef(0.22, 0.0, 0.0)
            glScalef(0.08, 1.8, 0.3)
            Primitives.draw_textured_cube(1.0)
            glPopMatrix()


            glPopMatrix()

        # 3. Phase 2 Radial Shockwave Rings
        if phase == 2:
            glColor4f(1.0, 0.2, 0.4, 0.7)
            for ring_idx in range(2):
                glPushMatrix()
                glRotatef(anim_time * 160.0 * (1 if ring_idx == 0 else -1), 0.0, 1.0, 0.0)
                glRotatef(20.0 * ring_idx, 1.0, 0.0, 0.0)
                glutSolidTorus(0.06, 5.2, 8, 24)
                glPopMatrix()

        glPopMatrix()
