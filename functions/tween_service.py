#inspired by roblox tween services!!

from .easing_styles import (
    EasingStyle,
    EasingDirection,
    linear,
    quad,
)

class TweenInfo:
    def __init__(
        self, 
        dur,                    #Yeah it looks like i code weird or smth
        easing_style=EasingStyle.LINEAR,
        easing_direction=EasingDirection.IN,
    ):
        self.dur = max(0.0001, dur)
        self.easing_style = easing_style
        self.easing_direction = easing_direction


class Tween:
    def __init__(self, target, goals, tween_info): #Idk i keep on changing on how would i manage these "()" stuffs
        self.target = target
        self.goals = goals
        self.info = tween_info

        self.start_vals = {
            property_name: getattr(target, property_name)
            for property_name in goals

        }

        self.elapsed = 0.0
        self.playing = False
        self.completed = False
        self.on_complete = None


    def play(self):
        self.start_vals = {
            property_name: getattr(
                self.target,
                property_name
            )
            for property_name in self.goals
        }
        self.elapsed = 0.0
        self.playing = True
        self.completed = False
    
    def cancel(self):
        self.playing = False
    
    def update(self, dt):
        if not self.playing:
            return # i mean obviously

        self.elapsed += dt
        progress = min(1.0, self.elapsed / self.info.dur)

        eased_progress = TweenService.evaluate(
            self.info,
            progress
        )


        for property_name, end_value in self.goals.items():
            start_vals = self.start_vals[property_name]
            value = start_vals + (
                end_value - start_vals
            ) * eased_progress
            setattr(self.target, property_name, value)
        
        if progress >= 1.0:
            for property_name, end_value in self.goals.items():
                setattr(self.target, property_name, end_value)
            self.playing = False
            self.completed = True
            if self.on_complete:
                self.on_complete()

#yo i made so many typos smh

class TweenService:    # HEHEHE >:3
    def __init__(self):
        self.active_tweens = []

    @staticmethod #oh this one is new
    def evaluate(tween_info, progress):
        if tween_info.easing_style == EasingStyle.LINEAR:
            return linear(progress)
        if tween_info.easing_style == EasingStyle.QUAD:
            return quad(
                progress,
                tween_info.easing_direction
            )
        raise ValueError(
            f"Unkown easing style!! {tween_info.easing_style}"
        )

    def create(self, target, tween_info, goals, on_complete=None):
        tween = Tween(target,goals,tween_info)
        tween.on_complete = on_complete
        self.active_tweens.append(tween)
        return tween

    def update(self, dt):
        for tween in self.active_tweens:
            tween.update(dt)
        
        self.active_tweens = [
            tween
            for tween in self.active_tweens
            if tween.playing
        ]