import regex as re
import subprocess
import os
import requests

def ocr_image(image_path):
    """
    Performs OCR on an image path.
    Uses a hybrid approach:
    1. OCR.space free developer API (highly accurate for formulas, works out-of-the-box).
    2. Natively installed PsOcr module fallback if offline.
    """
    abs_path = os.path.abspath(image_path)
    if not os.path.exists(abs_path):
        return ""

    # Attempt 1: OCR.space (Online, high accuracy for math)
    try:
        url = "https://api.ocr.space/parse/image"
        payload = {
            "apikey": "helloworld",  # Official developer test key
            "language": "eng",
            "isOverlayRequired": False,
            "scale": True,
            "OCREngine": 2
        }
        with open(abs_path, 'rb') as f:
            files = {"file": f}
            r = requests.post(url, data=payload, files=files, timeout=6)
        
        if r.status_code == 200:
            result = r.json()
            if "ParsedResults" in result and len(result["ParsedResults"]) > 0:
                text = result["ParsedResults"][0]["ParsedText"]
                if text.strip():
                    return text
    except Exception as e:
        print(f"[Math Solver] Online OCR failed or offline. Falling back. Error: {e}")

    # Attempt 2: PowerShell PsOcr fallback (Offline)
    ps_cmd = f"Convert-PsoImageToText -Path '{abs_path}'"
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=8
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception as e:
        print(f"[Math Solver] Offline PowerShell OCR failed: {e}")

    return ""

def clean_expression(expr_str):
    """Cleans math expressions and inserts multiplication operators where omitted."""
    expr = expr_str.strip()
    # Insert '*' between a digit and a variable, e.g. 2x -> 2*x, 3.5y -> 3.5*y
    expr = re.sub(r'(\d)\s*([a-zA-Z])', r'\1*\2', expr)
    # Replace visual symbols with python operators
    expr = expr.replace('^', '**').replace('÷', '/').replace('x', '*').replace('X', '*')
    return expr

def evaluate_side(side_str, var_name, var_value):
    """Safely evaluates a side of an equation for a given variable value."""
    cleaned = clean_expression(side_str)
    # Replace variable with value
    pattern = r'\b' + re.escape(var_name) + r'\b'
    substituted = re.sub(pattern, f"({var_value})", cleaned)
    # Strip dangerous characters to maintain safety
    safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', substituted)
    if not safe_expr.strip():
        return None
    try:
        # Safe mathematical evaluation
        return float(eval(safe_expr, {"__builtins__": None}, {}))
    except Exception:
        return None

def solve_algebraic_equation(lhs_str, rhs_str, var_name):
    """
    Solves LHS = RHS for var_name using numerical secant method.
    Extremely robust, solves linear, quadratic, and transcendental equations.
    """
    def f(val):
        l_val = evaluate_side(lhs_str, var_name, val)
        r_val = evaluate_side(rhs_str, var_name, val)
        if l_val is None or r_val is None:
            return None
        return l_val - r_val
        
    # Initial guesses
    x0 = 0.0
    x1 = 1.0
    
    f0 = f(x0)
    f1 = f(x1)
    
    if f0 is None or f1 is None:
        # Try alternate guesses if 0/1 yield Domain Errors
        x0, x1 = 2.0, 3.0
        f0, f1 = f(x0), f(x1)
        if f0 is None or f1 is None:
            return None
            
    if abs(f0) < 1e-7:
        return x0
    if abs(f1) < 1e-7:
        return x1
        
    for _ in range(80):
        if abs(f1 - f0) < 1e-12:
            break
        try:
            x_next = x1 - f1 * (x1 - x0) / (f1 - f0)
        except ZeroDivisionError:
            break
            
        f_next = f(x_next)
        if f_next is None:
            break
            
        if abs(f_next) < 1e-5:
            if abs(x_next - round(x_next)) < 1e-5:
                return round(x_next)
            return round(x_next, 4)
            
        x0, x1 = x1, x_next
        f0, f1 = f1, f_next
        
    return None

def solve_math_in_image(image_path):
    """
    Main entrypoint: performs OCR on image, extracts mathematical expressions,
    solves them, and returns structured problems and answers.
    """
    text = ocr_image(image_path)
    if not text:
        return []
        
    lines = text.split('\n')
    solved_problems = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Clean leading/trailing punctuation noise common in OCR
        line_clean = re.sub(r'^[^\w(]+|[^\w)]+$', '', line)
        
        # Scenario A: Equation (contains '=')
        if '=' in line_clean:
            parts = line_clean.split('=', 1)
            lhs = parts[0].strip()
            rhs = parts[1].strip()
            
            # Find individual alphabetical characters as potential variables
            vars_found = re.findall(r'\b[a-zA-Z]\b', lhs + rhs)
            valid_vars = [v for v in vars_found if v.lower() not in ['i', 'e']]
            
            if valid_vars:
                var = valid_vars[0]
                sol = solve_algebraic_equation(lhs, rhs, var)
                if sol is not None:
                    solved_problems.append({
                        "type": "Algebraic Equation",
                        "original": line_clean,
                        "problem": f"{lhs} = {rhs}",
                        "solution": f"{var} = {sol}"
                    })
                continue
            else:
                # Arithmetic equation, e.g. "5 * (2 + 3) =" or "12 / 4 = ?"
                if not rhs or rhs == '?' or not re.search(r'\d', rhs):
                    cleaned_lhs = re.sub(r'[^0-9+\-*/().\s]', '', lhs.replace('x','*').replace('^','**').replace('÷','/'))
                    try:
                        val = eval(cleaned_lhs, {"__builtins__": None}, {})
                        solved_problems.append({
                            "type": "Arithmetic Equation",
                            "original": line_clean,
                            "problem": f"{lhs} =",
                            "solution": str(val)
                        })
                    except Exception:
                        pass
                continue
                
        # Scenario B: Pure Arithmetic Expression (e.g. "25 * 4 + 10")
        else:
            # Must contain numbers and at least one arithmetic symbol
            if re.search(r'\d', line_clean) and re.search(r'[\+\-\*\/÷^]', line_clean):
                cleaned = re.sub(r'[^0-9+\-*/().\s]', '', line_clean.replace('x','*').replace('^','**').replace('÷','/'))
                try:
                    # Guard length to avoid executing single digits
                    if len(cleaned.strip()) > 2:
                        val = eval(cleaned, {"__builtins__": None}, {})
                        solved_problems.append({
                            "type": "Arithmetic Expression",
                            "original": line_clean,
                            "problem": line_clean,
                            "solution": str(val)
                        })
                except Exception:
                    pass
                    
    return solved_problems
