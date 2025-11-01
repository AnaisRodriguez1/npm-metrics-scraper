import esprima
from npm_metrics_package.pipelines import LocalCodeAnalysisPipeline

# Simple test for the AST function counter
def test_count_functions():
    pipeline = LocalCodeAnalysisPipeline()
    
    # Test Case 1: Function declarations
    code1 = """
    function hello() {
        return "world";
    }
    
    function goodbye() {
        return "see you";
    }
    """
    tree1 = esprima.parseScript(code1)
    assert pipeline.count_functions_in_ast(tree1) == 2, "Should count 2 function declarations"
    print("Test 1 passed: Function declarations")
    
    # Test Case 2: Arrow functions
    code2 = """
    const add = (a, b) => a + b;
    const multiply = (x, y) => x * y;
    """
    tree2 = esprima.parseScript(code2)
    assert pipeline.count_functions_in_ast(tree2) == 2, "Should count 2 arrow functions"
    print("Test 2 passed: Arrow functions")
    
    # Test Case 3: Class methods
    code3 = """
    class Calculator {
        add(a, b) {
            return a + b;
        }
        
        subtract(a, b) {
            return a - b;
        }
    }
    """
    tree3 = esprima.parseScript(code3)
    assert pipeline.count_functions_in_ast(tree3) == 2, "Should count 2 class methods"
    print("Test 3 passed: Class methods")
    
    # Test Case 4: Mixed function types
    code4 = """
    function regularFunc() {}
    const arrowFunc = () => {};
    
    class MyClass {
        method() {}
    }
    """
    tree4 = esprima.parseScript(code4)
    assert pipeline.count_functions_in_ast(tree4) == 3, "Should count 3 functions (mixed types)"
    print("Test 4 passed: Mixed function types")
    
    # Test Case 5: Nested functions
    code5 = """
    function outer() {
        function inner() {
            return "nested";
        }
        return inner;
    }
    """
    tree5 = esprima.parseScript(code5)
    assert pipeline.count_functions_in_ast(tree5) == 2, "Should count nested functions"
    print("Test 5 passed: Nested functions")
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_count_functions()
