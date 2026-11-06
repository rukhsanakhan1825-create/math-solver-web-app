import sympy as sp
from sympy import (
    symbols, solve, diff, integrate, limit, simplify, factor,
    expand, sympify, latex, sqrt, pi, E, oo, Symbol,
    sin, cos, tan, log, exp, Rational, Matrix
)

import re
import statistics


x, y, z = symbols('x y z')


def detect_type(problem: str) -> str:
    """Auto-detect the type of math problem."""
    p = problem.lower().strip()

    if any(kw in p for kw in ["d/dx", "derivative", "differentiate", "diff("]):
        return "calculus_derivative"
    if any(kw in p for kw in ["integrate", "integral", "antiderivative", "∫"]):
        return "calculus_integral"
    if any(kw in p for kw in ["limit", "lim"]):
        return "calculus_limit"
    if any(kw in p for kw in ["mean", "median", "mode", "variance", "std", "standard deviation"]):
        return "statistics"
    if re.search(r"[a-zA-Z]", p) and any(op in p for op in ["=", "solve", "find x", "find y"]):
        return "algebra"
    if any(kw in p for kw in ["factor", "expand", "simplify"]):
        return "algebra"
    if re.search(r"[a-zA-Z]", p):
        return "algebra"
    return "arithmetic"


def solve_math(problem: str, problem_type: str = "auto") -> dict:
    """Main solver dispatcher."""
    try:
        if problem_type == "auto":
            problem_type = detect_type(problem)

        if problem_type == "arithmetic":
            return solve_arithmetic(problem)
        elif problem_type == "algebra":
            return solve_algebra(problem)
        elif problem_type == "calculus_derivative":
            return solve_derivative(problem)
        elif problem_type == "calculus_integral":
            return solve_integral(problem)
        elif problem_type == "calculus_limit":
            return solve_limit(problem)
        elif problem_type == "statistics":
            return solve_statistics(problem)
        else:
            return solve_arithmetic(problem)

    except Exception as e:
        return {"error": f"Could not solve: {str(e)}. Please check your input format."}


# ─── ARITHMETIC ────────────────────────────────────────────────────────────────

def solve_arithmetic(problem: str) -> dict:
    """Solve arithmetic expressions step by step."""
    steps = []
    original = problem.strip()

    # Clean and prepare
    expr_str = original.replace("^", "**").replace("×", "*").replace("÷", "/")
    steps.append(f"Original expression: {original}")

    # Evaluate with sympy for precision
    expr = sympify(expr_str)
    steps.append(f"Parsed expression: {expr}")

    # Show intermediate steps for basic operations
    result = float(expr.evalf())

    if "+" in expr_str:
        steps.append("Identify addition operation")
    if "-" in expr_str:
        steps.append("Identify subtraction operation")
    if "*" in expr_str:
        steps.append("Apply multiplication (higher precedence)")
    if "/" in expr_str:
        steps.append("Apply division (higher precedence)")
    if "**" in expr_str:
        steps.append("Apply exponentiation (highest precedence)")

    steps.append(f"Apply order of operations (PEMDAS/BODMAS)")
    steps.append(f"Final result: {expr} = {result if result != int(result) else int(result)}")

    display_result = int(result) if result == int(result) else round(result, 6)

    return {
        "type": "arithmetic",
        "problem": original,
        "result": str(display_result),
        "latex": f"{latex(expr)} = {display_result}",
        "steps": steps,
        "graph_data": None
    }


# ─── ALGEBRA ───────────────────────────────────────────────────────────────────

def solve_algebra(problem: str) -> dict:
    """Solve algebraic equations and expressions."""
    steps = []
    original = problem.strip()
    p = original.lower()

    steps.append(f"Problem: {original}")

    # Determine operation
    if "factor" in p:
        return solve_factor(original, steps)
    if "expand" in p:
        return solve_expand(original, steps)
    if "simplify" in p:
        return solve_simplify(original, steps)

    # Equation solving
    expr_str = original.replace("^", "**").replace("×", "*").replace("÷", "/")

    if "=" in expr_str:
        left, right = expr_str.split("=", 1)
        left_expr = sympify(left.strip().replace("^","**"))
        right_expr = sympify(right.strip().replace("^","**"))
        equation = left_expr - right_expr

        steps.append(f"Move all terms to left side: {latex(equation)} = 0")

        # Identify type
        degree = sp.degree(equation, x)
        if degree == 1:
            steps.append("Linear equation detected (degree 1)")
            steps.append("Isolate x by applying inverse operations")
        elif degree == 2:
            steps.append("Quadratic equation detected (degree 2)")
            steps.append("Apply quadratic formula or factoring")
        else:
            steps.append(f"Polynomial equation of degree {degree} detected")

        solutions = solve(equation, x)
        steps.append(f"Solve for x")
        steps.append(f"Solutions found: x = {', '.join([str(s) for s in solutions])}")

        # Verify
        for sol in solutions:
            verification = equation.subs(x, sol)
            steps.append(f"Verify x = {sol}: substituting gives {simplify(verification)} ✓")

        result_str = ", ".join([str(s) for s in solutions])
        latex_result = ", ".join([f"x = {latex(s)}" for s in solutions])

        # Graph data for quadratic
        graph_data = None
        if degree <= 3:
            graph_data = make_graph_data(equation, -10, 10)

        return {
            "type": "algebra",
            "problem": original,
            "result": f"x = {result_str}",
            "latex": latex_result,
            "steps": steps,
            "graph_data": graph_data
        }

    else:
        # Just simplify the expression
        expr = sympify(expr_str)
        simplified = simplify(expr)
        steps.append(f"Simplify the expression")
        steps.append(f"Result: {latex(simplified)}")
        return {
            "type": "algebra",
            "problem": original,
            "result": str(simplified),
            "latex": latex(simplified),
            "steps": steps,
            "graph_data": None
        }


def solve_factor(original, steps):
    p = original.lower().replace("factor", "").replace("(", "").replace(")", "").strip()
    expr_str = p.replace("^", "**")
    expr = sympify(expr_str)
    steps.append(f"Expression to factor: {latex(expr)}")
    factored = factor(expr)
    steps.append(f"Find common factors and group terms")
    steps.append(f"Factored form: {latex(factored)}")
    return {"type": "algebra", "problem": original, "result": str(factored),
            "latex": latex(factored), "steps": steps, "graph_data": None}


def solve_expand(original, steps):
    p = original.lower().replace("expand", "").strip()
    expr_str = p.replace("^", "**")
    expr = sympify(expr_str)
    steps.append(f"Expression to expand: {latex(expr)}")
    expanded = expand(expr)
    steps.append(f"Apply distributive property (FOIL for binomials)")
    steps.append(f"Expanded form: {latex(expanded)}")
    return {"type": "algebra", "problem": original, "result": str(expanded),
            "latex": latex(expanded), "steps": steps, "graph_data": None}


def solve_simplify(original, steps):
    p = original.lower().replace("simplify", "").strip()
    expr_str = p.replace("^", "**")
    expr = sympify(expr_str)
    steps.append(f"Expression: {latex(expr)}")
    simplified = simplify(expr)
    steps.append(f"Apply algebraic identities and simplification rules")
    steps.append(f"Simplified: {latex(simplified)}")
    return {"type": "algebra", "problem": original, "result": str(simplified),
            "latex": latex(simplified), "steps": steps, "graph_data": None}


# ─── CALCULUS ──────────────────────────────────────────────────────────────────

def solve_derivative(problem: str) -> dict:
    """Compute derivative with steps."""
    steps = []
    original = problem.strip()
    steps.append(f"Problem: Find the derivative of {original}")

    # Extract function
    p = original.lower()
    for kw in ["d/dx", "derivative of", "differentiate", "diff("]:
        p = p.replace(kw, "").strip()

    expr_str = p.replace("^", "**").strip("() ")
    expr = sympify(expr_str)
    steps.append(f"Function: f(x) = {latex(expr)}")

    # Identify rules used
    if expr.is_Add:
        steps.append("Apply Sum Rule: d/dx[f+g] = f' + g'")
    if expr.is_Mul:
        steps.append("Apply Product Rule: d/dx[f·g] = f'g + fg'")
    if isinstance(expr, sp.Pow):
        steps.append("Apply Power Rule: d/dx[xⁿ] = n·xⁿ⁻¹")
    if expr.has(sin) or expr.has(cos):
        steps.append("Apply Trigonometric derivative rules")
    if expr.has(log):
        steps.append("Apply Logarithm derivative: d/dx[ln(x)] = 1/x")
    if expr.has(exp):
        steps.append("Apply Exponential rule: d/dx[eˣ] = eˣ")

    derivative = diff(expr, x)
    derivative_simplified = simplify(derivative)

    steps.append(f"Compute derivative term by term")
    steps.append(f"f'(x) = {latex(derivative_simplified)}")

    graph_data = make_graph_data_two(expr, derivative_simplified, -5, 5)

    return {
        "type": "calculus_derivative",
        "problem": original,
        "result": str(derivative_simplified),
        "latex": f"f'(x) = {latex(derivative_simplified)}",
        "steps": steps,
        "graph_data": graph_data
    }


def solve_integral(problem: str) -> dict:
    """Compute integral with steps."""
    steps = []
    original = problem.strip()
    steps.append(f"Problem: Integrate {original}")

    p = original.lower()
    for kw in ["integrate", "integral of", "antiderivative of", "∫"]:
        p = p.replace(kw, "").strip()

    expr_str = p.replace("^", "**").strip("() ")
    # Remove 'dx' if present
    expr_str = re.sub(r'\s*d[xyz]\s*$', '', expr_str).strip()

    expr = sympify(expr_str)
    steps.append(f"Function: f(x) = {latex(expr)}")
    steps.append(f"Find the antiderivative F(x) such that F'(x) = f(x)")

    if isinstance(expr, sp.Pow) and expr.args[0] == x:
        n = expr.args[1]
        steps.append(f"Apply Power Rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C")
    elif expr.has(sin) or expr.has(cos):
        steps.append("Apply standard trigonometric integral formulas")
    elif expr.has(exp):
        steps.append("Apply exponential integral: ∫eˣ dx = eˣ + C")
    elif expr.has(log):
        steps.append("Apply integration by parts or substitution")
    else:
        steps.append("Apply appropriate integration technique")

    integral = integrate(expr, x)
    integral_simplified = simplify(integral)

    steps.append(f"Compute the integral")
    steps.append(f"∫f(x) dx = {latex(integral_simplified)} + C")
    steps.append("Add constant of integration C (indefinite integral)")

    return {
        "type": "calculus_integral",
        "problem": original,
        "result": str(integral_simplified) + " + C",
        "latex": f"\\int {latex(expr)}\\, dx = {latex(integral_simplified)} + C",
        "steps": steps,
        "graph_data": make_graph_data(expr, -5, 5)
    }


def solve_limit(problem: str) -> dict:
    """Compute limit with steps."""
    steps = []
    original = problem.strip()
    steps.append(f"Problem: {original}")

    # Try to parse: "limit of x^2 as x->2" or "lim x->0 sin(x)/x"
    p = original.lower().replace("limit of", "").replace("lim", "").strip()

    # Extract x-> value
    match = re.search(r'x\s*->\s*([^\s,]+)', p)
    if not match:
        return {"error": "Please format as: limit of [expression] as x->value"}

    point_str = match.group(1).replace("inf", "oo").replace("∞", "oo")
    point = sympify(point_str)

    # Extract expression
    expr_str = re.sub(r'as\s+x\s*->\s*[^\s,]+', '', p)
    expr_str = re.sub(r'x\s*->\s*[^\s,]+', '', expr_str).strip()
    expr_str = expr_str.replace("^", "**")
    expr = sympify(expr_str)

    steps.append(f"Evaluate: lim x→{point_str} of {latex(expr)}")
    steps.append(f"First try direct substitution: x = {point_str}")

    try:
        direct = expr.subs(x, point)
        direct_simplified = simplify(direct)
        if direct_simplified not in [sp.zoo, sp.nan, oo, -oo]:
            steps.append(f"Direct substitution gives: {latex(direct_simplified)}")
        else:
            steps.append(f"Direct substitution gives indeterminate form — apply L'Hôpital or algebraic simplification")
    except:
        steps.append("Direct substitution undefined — apply L'Hôpital or simplification")

    result = limit(expr, x, point)
    steps.append(f"Evaluate the limit")
    steps.append(f"lim x→{point_str} [{latex(expr)}] = {latex(result)}")

    return {
        "type": "calculus_limit",
        "problem": original,
        "result": str(result),
        "latex": f"\\lim_{{x \\to {latex(point)}}} {latex(expr)} = {latex(result)}",
        "steps": steps,
        "graph_data": make_graph_data(expr, -10, 10)
    }


# ─── STATISTICS ────────────────────────────────────────────────────────────────

def solve_statistics(problem: str) -> dict:
    """Solve statistics problems."""
    steps = []
    original = problem.strip()
    p = original.lower()
    steps.append(f"Problem: {original}")

    # Extract numbers
    numbers = list(map(float, re.findall(r'-?\d+\.?\d*', original)))
    if not numbers:
        return {"error": "No numbers found. Please provide a list of numbers."}

    steps.append(f"Data set: {numbers}")
    steps.append(f"n = {len(numbers)} values")

    results = {}

    if "mean" in p or "average" in p:
        m = statistics.mean(numbers)
        steps.append(f"Mean = sum of all values / n = {sum(numbers)} / {len(numbers)} = {m}")
        results["Mean"] = round(m, 4)

    if "median" in p:
        sorted_nums = sorted(numbers)
        med = statistics.median(numbers)
        steps.append(f"Sort data: {sorted_nums}")
        steps.append(f"Median = middle value = {med}")
        results["Median"] = med

    if "mode" in p:
        try:
            mode = statistics.mode(numbers)
            steps.append(f"Mode = most frequent value = {mode}")
            results["Mode"] = mode
        except:
            steps.append("No unique mode found (multiple modes or all values unique)")

    if "variance" in p or "var" in p:
        var = statistics.variance(numbers)
        steps.append(f"Variance = Σ(xᵢ - mean)² / (n-1) = {round(var, 4)}")
        results["Variance"] = round(var, 4)

    if "std" in p or "standard deviation" in p:
        std = statistics.stdev(numbers)
        mean_val = statistics.mean(numbers)
        steps.append(f"Standard Deviation = √Variance = {round(std, 4)}")
        results["Std Dev"] = round(std, 4)

    # If no specific keyword, compute all
    if not results:
        mean_val = statistics.mean(numbers)
        med = statistics.median(numbers)
        var = statistics.variance(numbers) if len(numbers) > 1 else 0
        std = statistics.stdev(numbers) if len(numbers) > 1 else 0
        results = {
            "Mean": round(mean_val, 4),
            "Median": med,
            "Variance": round(var, 4),
            "Std Dev": round(std, 4),
            "Min": min(numbers),
            "Max": max(numbers),
            "Range": max(numbers) - min(numbers)
        }
        steps.append(f"Computed all descriptive statistics")
        for k, v in results.items():
            steps.append(f"{k} = {v}")

    result_str = " | ".join([f"{k}: {v}" for k, v in results.items()])

    return {
        "type": "statistics",
        "problem": original,
        "result": result_str,
        "latex": result_str,
        "steps": steps,
        "graph_data": None,
        "stats_results": results
    }


# ─── GRAPH HELPERS ─────────────────────────────────────────────────────────────

def make_graph_data(expr, x_min, x_max, points=100):
    """Generate graph data points for a single expression."""
    try:
        f = sp.lambdify(x, expr, "math")
        xs = [x_min + (x_max - x_min) * i / points for i in range(points + 1)]
        ys = []
        for xi in xs:
            try:
                yi = f(xi)
                ys.append(round(yi, 4) if abs(yi) < 1e6 else None)
            except:
                ys.append(None)
        return {"labels": [round(xi, 2) for xi in xs], "datasets": [{"label": str(expr), "data": ys}]}
    except:
        return None


def make_graph_data_two(f_expr, df_expr, x_min, x_max, points=100):
    """Generate graph data for function and its derivative."""
    try:
        f = sp.lambdify(x, f_expr, "math")
        df = sp.lambdify(x, df_expr, "math")
        xs = [x_min + (x_max - x_min) * i / points for i in range(points + 1)]
        ys_f, ys_df = [], []
        for xi in xs:
            try:
                yi = f(xi)
                ys_f.append(round(yi, 4) if abs(yi) < 1e6 else None)
            except:
                ys_f.append(None)
            try:
                yi2 = df(xi)
                ys_df.append(round(yi2, 4) if abs(yi2) < 1e6 else None)
            except:
                ys_df.append(None)
        return {
            "labels": [round(xi, 2) for xi in xs],
            "datasets": [
                {"label": f"f(x) = {str(f_expr)}", "data": ys_f, "color": "blue"},
                {"label": f"f'(x) = {str(df_expr)}", "data": ys_df, "color": "red"}
            ]
        }
    except:
        return None
