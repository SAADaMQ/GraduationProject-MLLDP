"""
theme configuration
deep navy + royal gold banking aesthetic
"""

# primary palette
PRIMARY_NAVY = "#0A2540"
ROYAL_GOLD = "#C9A961"
PEARL_WHITE = "#FAFAFA"
CHARCOAL = "#1F2937"

# zone colors
COLOR_APPROVE = "#10B981"
COLOR_HIGH_RISK = "#F59E0B"
COLOR_REJECT = "#DC2626"

# global css to inject into every page
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

h1, h2, h3, h4 {
    color: #0A2540;
    font-weight: 600;
}

.stButton button {
    background-color: #0A2540;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: all 200ms ease;
}

.stButton button:hover {
    background-color: #C9A961;
    color: #0A2540;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
"""