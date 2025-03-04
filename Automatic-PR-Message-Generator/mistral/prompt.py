class Prompt:
    def __init__(self, diff_analysis, pr_summary):
        """
        Initializes the prompt with diff analysis and PR summary.
        """
        self.diff_analysis = diff_analysis  # Expecting this to be a list of dictionaries
        self.pr_summary = pr_summary
        self.text = self._create_prompt_text()

    def _create_prompt_text(self):
        """
        Create the prompt text based on the diff analysis.
        """
        prompt_text = f"### PR Summary:\n{self.pr_summary}\n\n"
        prompt_text += "### Code Changes:\n"
        prompt_text += """  
**Analyze the Pull Request details and assign a score between 0 and 100 for each category listed below**. Use the provided rubric for guidance. Ensure that scores reflect the quality and specifics of the Pull Request, and do not bias scores toward high values without sufficient justification. Follow the exact format given below:

#### **Scoring Rubric**:
- **100**: Excellent, exceeds all expectations, no areas for improvement.  
- **80–99**: Very good, meets most expectations with minor improvements needed.  
- **60–79**: Satisfactory, meets minimum expectations but requires moderate improvement.  
- **40–59**: Below average, significant improvements needed.  
- **0–39**: Poor, fails to meet expectations.

#### **Scoring Categories**:
- **Category 1: Impact Analysis**  
  Evaluate the impact of the Pull Request on the overall codebase using these factors:  
  - **Bug Fix**: How effectively it resolves existing issues or bugs.  
  - **Usefulness**: The value the changes add to the project.  
  - **New Functionality**: How the new features enhance the system.  
  - **Maintainability**: The impact on the code’s maintainability and long-term stability.  

  **Impact Score**: Overall score based on Bug Fix, Usefulness, New Functionality and Maintainability[0–100]  

---

- **Category 2: Code Quality**  
  Assess the overall quality of the code using factors such as readability, structure, and adherence to best practices.  

  **Code Quality Score**: [0–100]  

---

- **Category 3: Security**  
  Identify any security vulnerabilities or risks introduced by the code (e.g., hardcoded credentials, unsafe serialization, SQL injection).  

  **Security Score**: [0–100]  

---

- **Category 4: Creativity**  
  Determine originality and innovation. Unique and creative code gets a high score; unoriginal or heavily copied code gets a low score.  

  **Creativity Score**: [0–100]  

---

### **Few-Shot Examples for your understanding of the rubrics (This is not a PR change)**:

**Example 1:**  
- **PR Summary**:  
  PR #123: Refactor the user authentication system.  
- **Code Changes**:  
  Added JWT-based token authentication, removed legacy session-based authentication, and updated relevant endpoints.  

  **Description**:  
  Refactored the authentication system to enhance security by introducing JWT tokens. Deprecated session-based authentication and replaced it with token-based mechanisms, improving scalability. Updated endpoints and associated documentation.  

  **Impact Score**: 90  
  - **Reasoning**: Significantly enhances security and scalability. However, backward compatibility with existing systems might require additional consideration.  

  **Code Quality Score**: 85  
  - **Reasoning**: Well-structured and readable code but could benefit from more extensive documentation.  

  **Security Score**: 95  
  - **Reasoning**: Eliminates session vulnerabilities and implements JWT securely.  

  **Creativity Score**: 80  
  - **Reasoning**: Implements known best practices effectively but does not introduce novel approaches.  

---

**Example 2:**  
- **PR Summary**:  
  PR #124: Add caching for frequently accessed endpoints.  
- **Code Changes**:  
  Implemented Redis caching for GET /products and GET /categories, reducing response times by 70%.  

  **Description**:  
  Added Redis-based caching to optimize the performance of frequently accessed endpoints. Updated configuration files and ensured cache invalidation works seamlessly.  

  **Impact Score**: 85  
  - **Reasoning**: Greatly improves performance but limited to a specific use case.  

  **Code Quality Score**: 88  
  - **Reasoning**: Follows best practices, though inline comments could be clearer.  

  **Security Score**: 80  
  - **Reasoning**: No security vulnerabilities, but configuration files could be better secured.  

  **Creativity Score**: 75  
  - **Reasoning**: Effectively applies an established approach without significant innovation.  

---

**Now, evaluate the given Pull Request using the above format and rubric.**

Here are additional examples to guide the LLM further:

---

**Example 3:**  
- **PR Summary**:  
  PR #125: Add a new feature to support dark mode in the user interface.  
- **Code Changes**:  
  Introduced a toggle switch for dark mode in the UI settings. Updated CSS styles for dark mode compatibility across all pages. Added tests for dark mode activation and ensured accessibility compliance.  

  **Description**:  
  Added a dark mode feature, allowing users to switch between light and dark themes. Updated stylesheets to ensure consistent visual presentation in both modes. Included accessibility enhancements like color contrast adjustments and screen reader support.  

  **Impact Score**: 95  
  - **Reasoning**: Highly useful and improves user experience significantly. Well-implemented with accessibility considerations.  

  **Code Quality Score**: 90  
  - **Reasoning**: Clear and modular code, though minor documentation improvements are needed.  

  **Security Score**: 100  
  - **Reasoning**: No security risks introduced.  

  **Creativity Score**: 85  
  - **Reasoning**: A creative solution to enhance user experience with proper accessibility support.  

---

Here’s another concise example:

---

**Example 4:**  
- **PR Summary**: PR #127: Optimize database queries for user activity reports.  
- **Code Changes**: Refactored SQL queries to reduce redundant joins, added proper indexing to relevant tables, and optimized pagination for large datasets.  

  **Description**: Improved query efficiency for generating user activity reports. Reduced load times by 60% through indexing and optimized joins. Enhanced pagination for better performance on large datasets.  

  **Impact Score**: 90  
  - **Reasoning**: Significant improvement in performance with a noticeable impact on large datasets.  

  **Code Quality Score**: 88  
  - **Reasoning**: Clean and efficient SQL, though code comments could be more detailed for future maintainability.  

  **Security Score**: 95  
  - **Reasoning**: Eliminated potential SQL injection risks and validated query inputs.  

  **Creativity Score**: 80  
  - **Reasoning**: Effective optimization using established database techniques.  

---"""


        for file_change in self.diff_analysis:
            file_name = file_change.get("file", "Unknown file")
            prompt_text += f"  - {file_name}:\n"
            for change in file_change.get("changes", []):
                change_type = change.get("type", "Unknown")
                content = change.get("content", "")
                prompt_text += f"    {change_type.capitalize()}: {content}\n"

        return prompt_text
