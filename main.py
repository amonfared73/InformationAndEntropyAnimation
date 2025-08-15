from manim import *
import math

class Title(Scene):
    def construct(self):

        firstPart = Text("Information", font_size=48)
        secondPart = Text("is", font_size=48)
        thirdPart = Text("Surprise!!", font_size=72, color=BLUE)

        title = VGroup(firstPart, secondPart, thirdPart).arrange(RIGHT, buff=0.5)

        self.play(Write(firstPart))
        self.wait(0.5)
        self.play(Write(secondPart))
        self.wait(0.5)
        self.play(Write(thirdPart))
        self.wait(1)

class SimpleCoinFlip(Scene):
    def construct(self):

        SILVER = "#C0C0C0"

        prob_heads = MathTex("P(\\text{Heads}) = \\frac{1}{2}", font_size=28)
        prob_tails = MathTex("P(\\text{Tails}) = \\frac{1}{2}", font_size=28)
        formulas = VGroup(prob_heads, prob_tails).arrange(DOWN, buff=0.3)
        formulas.to_corner(UL)  # UL = upper-left corner

        self.play(Write(prob_heads))
        self.wait(0.5)
        self.play(Write(prob_tails))
        self.wait(0.5)

        coin_front = Circle(radius=2, color=GOLD, fill_opacity=1)
        coin_front.set_fill(GOLD_E)
        heads_text = Text("Heads", font_size=36, color=BLACK)
        front_group = VGroup(coin_front, heads_text)

        coin_back = Circle(radius=2, color=SILVER, fill_opacity=1)
        coin_back.set_fill(SILVER)
        tails_text = Text("Tails", font_size=36, color=BLACK)
        back_group = VGroup(coin_back, tails_text)

        coin_group = front_group
        self.play(FadeIn(coin_group))

        def flip():
            nonlocal coin_group
            self.play(coin_group.animate.scale([0.05, 1, 1]), run_time=0.8, rate_func=smooth)
            self.remove(coin_group)
            coin_group = back_group if coin_group == front_group else front_group
            self.add(coin_group.scale([0.05, 1, 1]))
            self.play(coin_group.animate.scale([20, 1, 1]), run_time=0.8, rate_func=smooth)

        for _ in range(1):
            flip()

        self.wait()

class InformationFormula(Scene):
    def construct(self):
        title = Text("Information", font_size=48).to_edge(UP)
        self.play(Write(title))

        formula = MathTex("I(x) = -\\log(p(x))", font_size=72)

        self.play(Write(formula, run_time=2))
        self.wait(2)

        title = Text("p(x) = probability of event x", font_size=28).to_edge(DOWN)
        self.play(Write(title))
        self.wait(2)
        
        
class SimpleCoinInformation(Scene):
    def construct(self):
        title = Text(
            "Information gained by flipping a coin",
            font_size=48
        )
        heads_text = Text(
            "P(Heads) = 0.5,  I(Heads) = -log(0.5) = 1 bit",
            font_size=28
        )
        tails_text = Text(
            "P(Tails) = 0.5,  I(Tails) = -log(0.5) = 1 bit",
            font_size=28
        )

        group = VGroup(title, heads_text, tails_text)
        group.arrange(DOWN, buff=0.8)  # buff = space between lines
        group.move_to(ORIGIN)  

        self.play(Write(title))
        self.wait(1)
        self.play(Write(heads_text))
        self.wait(1)
        self.play(Write(tails_text))
        self.wait(2)


class SimpleDiceInformation(Scene):
    def construct(self):
        title = Text("Information Gain from Tossing a Dice").scale(0.8).to_edge(UP)
        self.play(Write(title))
        
        pip_positions = {
            1: [(0,0,0)],
            2: [(-0.3,0.3,0), (0.3,-0.3,0)],
            3: [(-0.3,0.3,0), (0,0,0), (0.3,-0.3,0)],
            4: [(-0.3,0.3,0), (0.3,0.3,0), (-0.3,-0.3,0), (0.3,-0.3,0)],
            5: [(-0.3,0.3,0), (0.3,0.3,0), (0,0,0), (-0.3,-0.3,0), (0.3,-0.3,0)],
            6: [(-0.3,0.3,0), (0.3,0.3,0), (-0.3,0,0), (0.3,0,0), (-0.3,-0.3,0), (0.3,-0.3,0)]
        }
        
        def make_face(number):
            face = Square().set_fill(WHITE, opacity=1).set_stroke(BLACK, width=2)
            pips = VGroup(*[Dot(radius=0.12, color=BLACK).move_to(pos) for pos in pip_positions[number]])
            return VGroup(face, pips)
        
        all_faces = VGroup(*[make_face(i) for i in range(1,7)]).arrange(RIGHT, buff=0.3)
        self.play(FadeIn(all_faces))
        
        probs = VGroup(*[MathTex(r"P(x) = \frac{1}{6}").scale(0.6) for _ in range(6)])
        for prob, face in zip(probs, all_faces):
            prob.next_to(face, DOWN)
        self.play(*[Write(prob) for prob in probs])
        
        self.wait(1)
        
        info_formula = MathTex(r"I(P(x)) = -\log_2(P(x))").to_edge(DOWN)
        self.play(Write(info_formula))
        self.wait(1)
        
        calc_formula = MathTex(r"I\left(\frac{1}{6}\right) = -\log_2\left(\frac{1}{6}\right)").to_edge(DOWN)
        self.play(Transform(info_formula, calc_formula))
        self.wait(1)
        
        bits_value = round(-math.log2(1/6), 3)  # 2.585
        infos = VGroup(*[MathTex(f"{bits_value} \\, \\text{{bits}}").scale(0.6) for _ in range(6)])
        for info, face in zip(infos, all_faces):
            info.next_to(face, UP)
        
        self.play(*[FadeIn(info) for info in infos])
        self.wait(2)



class InformationFromProbability(Scene):
    def construct(self):
        def info_func(p):
            return -np.log2(p)

        axes = Axes(
            x_range=[0, 1.05, 0.1],
            y_range=[0, 3.5, 0.5],
            x_length=8,
            y_length=4.5,
            axis_config={"color": GREY_A},
            tips=False
        )

        graph = axes.plot(info_func, x_range=[0.001, 1], color=BLUE)
        graph_label = MathTex("I = -\\log_2(P)").next_to(graph, UP)

        y_label = axes.get_y_axis_label("I (bits)", edge=LEFT, direction=LEFT)
        x_label = axes.get_x_axis_label("P (probability)")
        x_label.next_to(graph, DOWN) 

        self.play(Create(axes), Write(y_label))
        self.play(Create(graph), Write(graph_label), Write(x_label))
        self.wait(0.5)

        P_tracker = ValueTracker(0.5)

        dot = always_redraw(lambda: Dot(
            color=RED,
            radius=0.08
        ).move_to(axes.c2p(P_tracker.get_value(), info_func(P_tracker.get_value())))
        )

        label = always_redraw(lambda: MathTex(
            f"P={P_tracker.get_value():.2f},\\ I={info_func(P_tracker.get_value()):.3f}"
        ).scale(0.7).next_to(dot, UP))

        self.add(dot, label)
        self.wait(1)

        self.play(P_tracker.animate.set_value(0.3), run_time=2)
        self.wait(1)
        self.play(P_tracker.animate.set_value(0.8), run_time=2)
        self.wait(1)
        self.play(P_tracker.animate.set_value(1.0), run_time=2)
        self.wait(1)


class BiasedCoinFlip(Scene):
    def construct(self):
        SILVER = "#C0C0C0"

        prob_heads = MathTex("P(\\text{Heads}) = \\frac{1}{4}", font_size=28)
        prob_tails = MathTex("P(\\text{Tails}) = \\frac{3}{4}", font_size=28)
        formulas = VGroup(prob_heads, prob_tails).arrange(DOWN, buff=0.3)
        formulas.to_corner(UL)  # UL = upper-left corner

        self.play(Write(prob_heads))
        self.wait(0.5)
        self.play(Write(prob_tails))
        self.wait(0.5)

        coin_front = Circle(radius=2, color=GOLD, fill_opacity=1)
        coin_front.set_fill(GOLD_E)
        heads_text = Text("Heads", font_size=36, color=BLACK)
        front_group = VGroup(coin_front, heads_text)

        coin_back = Circle(radius=2, color=SILVER, fill_opacity=1)
        coin_back.set_fill(SILVER)
        tails_text = Text("Tails", font_size=36, color=BLACK)
        back_group = VGroup(coin_back, tails_text)

        coin_group = front_group
        self.play(FadeIn(coin_group))

        def flip():
            nonlocal coin_group
            self.play(coin_group.animate.scale([0.05, 1, 1]), run_time=0.8, rate_func=smooth)
            self.remove(coin_group)
            coin_group = back_group if coin_group == front_group else front_group
            self.add(coin_group.scale([0.05, 1, 1]))  # Keep squashed for smoothness
            self.play(coin_group.animate.scale([20, 1, 1]), run_time=0.8, rate_func=smooth)

        for _ in range(1):
            flip()

        self.wait()

class BiasedCoinInformation(Scene):
    def construct(self):
        title = Text(
            "Information gained by flipping a coin",
            font_size=48
        )
        heads_text = Text(
            "P(Heads) = 0.25,  I(Heads) = -log(0.25) = 2 bit",
            font_size=28
        )
        tails_text = Text(
            "P(Tails) = 0.75,  I(Tails) = -log(0.75) = 0.415 bit",
            font_size=28
        )

        group = VGroup(title, heads_text, tails_text)
        group.arrange(DOWN, buff=0.8)  
        group.move_to(ORIGIN) 

        self.play(Write(title))
        self.wait(1)
        self.play(Write(heads_text))
        self.wait(1)
        self.play(Write(tails_text))
        self.wait(2)



class BiasedDiceInformation(Scene):
    def construct(self):
        title = Text("Information Gain from Tossing a Biased Dice").scale(0.8).to_edge(UP)
        self.play(Write(title))
        
        pip_positions = {
            1: [(0,0,0)],
            2: [(-0.3,0.3,0), (0.3,-0.3,0)],
            3: [(-0.3,0.3,0), (0,0,0), (0.3,-0.3,0)],
            4: [(-0.3,0.3,0), (0.3,0.3,0), (-0.3,-0.3,0), (0.3,-0.3,0)],
            5: [(-0.3,0.3,0), (0.3,0.3,0), (0,0,0), (-0.3,-0.3,0), (0.3,-0.3,0)],
            6: [(-0.3,0.3,0), (0.3,0.3,0), (-0.3,0,0), (0.3,0,0), (-0.3,-0.3,0), (0.3,-0.3,0)]
        }
        
        def make_face(number):
            face = Square().set_fill(WHITE, opacity=1).set_stroke(BLACK, width=2)
            pips = VGroup(*[Dot(radius=0.12, color=BLACK).move_to(pos) for pos in pip_positions[number]])
            return VGroup(face, pips)
        
        all_faces = VGroup(*[make_face(i) for i in range(1,7)]).arrange(RIGHT, buff=0.3)
        self.play(FadeIn(all_faces))
        
        probabilities = ["\\frac{1}{12}", "\\frac{1}{4}", "\\frac{1}{6}", "\\frac{1}{3}", "\\frac{1}{12}", "\\frac{1}{12}"]
        probabilities_float = [1/12, 1/4, 1/6, 1/3, 1/12, 1/12]  # for calculations
        
        probs = VGroup(*[MathTex(f"P({i+1}) = {prob}").scale(0.6) for i, prob in enumerate(probabilities)])
        for prob, face in zip(probs, all_faces):
            prob.next_to(face, DOWN)
        self.play(*[Write(prob) for prob in probs])
        self.wait(1)
        
        info_formula = MathTex(r"I(P(x)) = -\log_2(P(x))").to_edge(DOWN)
        self.play(Write(info_formula))
        self.wait(1)
        
        infos = VGroup()
        for prob_float, face in zip(probabilities_float, all_faces):
            info_value = round(-math.log2(prob_float), 3)
            value_tex = MathTex(f"{info_value}").scale(0.6)
            unit_text = Text(" bits").scale(0.4).next_to(value_tex, RIGHT, buff=0.05)
            info = VGroup(value_tex, unit_text)
            info.next_to(face, UP)
            infos.add(info)
        
        self.play(*[FadeIn(info) for info in infos])
        self.wait(2)
        
class LotteryInformation(Scene):
    def construct(self):
        title = Text("Lottery Surprise and Information", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        prob_win = MathTex(r"P(\text{win}) = \frac{1}{1{,}000{,}000}", font_size=36)
        prob_lose = MathTex(r"P(\text{lose}) \approx 0.999999", font_size=36)
        prob_win.next_to(title, DOWN, buff=1)
        prob_lose.next_to(prob_win, DOWN, buff=0.5)
        self.play(Write(prob_win), Write(prob_lose))
        self.wait(1)

        info_win = MathTex(r"I(\text{win}) = -\log_2(P(\text{win})) \approx 20 \text{ bits}", font_size=36)
        info_lose = MathTex(r"I(\text{lose}) = -\log_2(P(\text{lose})) \approx 0.0000014 \text{ bits}", font_size=36)
        info_win.next_to(prob_lose, DOWN, buff=0.7)
        info_lose.next_to(info_win, DOWN, buff=0.5)
        self.play(Write(info_win), Write(info_lose))
        self.wait(1.5)

        win_icon = Text("🏆💰", font_size=72, color=YELLOW).to_edge(LEFT, buff=1)
        lose_icon = Text("❌", font_size=72, color=RED).to_edge(RIGHT, buff=1)
        self.play(FadeIn(win_icon), FadeIn(lose_icon))
        self.wait(1)
        
        
class EntropyScene(Scene):
    def construct(self):
        title = MarkupText(
            "<span foreground='red'>Entropy</span>, the average <span foreground='blue'>surprise</span>"
        ).to_edge(UP)
        
        self.play(Write(title))
        self.wait(1)

        formula = MathTex(
            "H(X) = - \\sum_{i=1}^{n} P(x_i) \\log P(x_i)"
        ).move_to(ORIGIN)

        self.play(Write(formula))
        self.wait(2)


class CoinEntropyScene(Scene):
    def construct(self):
        fair_coin_formula = MathTex(
            "H_{fair} = - \\Big[ \\frac{1}{2} \\log_2 \\frac{1}{2} + \\frac{1}{2} \\log_2 \\frac{1}{2} \\Big]"
        ).scale(0.8)

        fair_coin_calc = MathTex(
            "H_{fair} = - \\Big[ 2 \\cdot \\frac{1}{2} \\cdot (-1) \\Big] = 1"
        ).scale(0.8)

        biased_coin_formula = MathTex(
            "H_{biased} = - \\Big[ \\frac{1}{4} \\log_2 \\frac{1}{4} + \\frac{3}{4} \\log_2 \\frac{3}{4} \\Big]"
        ).scale(0.8)

        biased_coin_calc = MathTex(
            "H_{biased} = - \\Big[ \\frac{1}{4}(-2) + \\frac{3}{4}(-0.415) \\Big] \\approx 0.811"
        ).scale(0.8)

        conclusion = Text(
            "Fair coin has higher entropy (more uncertainty)"
        ).scale(0.7)

        group = VGroup(
            fair_coin_formula,
            fair_coin_calc,
            biased_coin_formula,
            biased_coin_calc,
            conclusion
        ).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        self.play(Write(fair_coin_formula))
        self.wait(1)
        self.play(Write(fair_coin_calc))
        self.wait(1)
        self.play(Write(biased_coin_formula))
        self.wait(1)
        self.play(Write(biased_coin_calc))
        self.wait(1)
        self.play(FadeIn(conclusion))
        self.wait(2)
