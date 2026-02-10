import random
import arcade


def make_coin_emitter(x: float, y: float) -> arcade.Emitter:
    return arcade.Emitter(
        center_xy=(x, y),
        emit_controller=arcade.EmitBurst(count=15),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=":resources:images/items/coinGold.png",
            change_xy=(
                random.uniform(-3, 3),
                random.uniform(1, 5),
            ),
            lifetime=random.uniform(0.4, 0.8),
            scale=random.uniform(0.1, 0.2),
            change_angle=random.uniform(-5, 5),
        ),
    )


def make_enemy_emitter(x: float, y: float) -> arcade.Emitter:
    return arcade.Emitter(
        center_xy=(x, y),
        emit_controller=arcade.EmitBurst(count=20),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=":resources:images/pinball/pool_cue_ball.png",
            change_xy=(
                random.uniform(-4, 4),
                random.uniform(1, 6),
            ),
            lifetime=random.uniform(0.3, 0.7),
            scale=random.uniform(0.05, 0.15),
            change_angle=random.uniform(-6, 6),
        ),
    )


def make_hurt_emitter(x: float, y: float) -> arcade.Emitter:
    return arcade.Emitter(
        center_xy=(x, y),
        emit_controller=arcade.EmitBurst(count=10),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=":resources:images/items/gemRed.png",
            change_xy=(
                random.uniform(-3, 3),
                random.uniform(1, 4),
            ),
            lifetime=random.uniform(0.3, 0.6),
            scale=random.uniform(0.08, 0.15),
            change_angle=random.uniform(-4, 4),
        ),
    )
