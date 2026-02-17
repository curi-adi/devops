from flask import Flask, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aditya Shrivastava &mdash; Machine Learning Engineer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #e2e8f0;
            line-height: 1.7;
        }

        /* -- Nav -- */
        nav {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid #1e293b;
            padding: 16px 0;
        }
        nav ul {
            list-style: none;
            max-width: 900px;
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            justify-content: center;
            gap: 32px;
        }
        nav a {
            color: #94a3b8;
            text-decoration: none;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            transition: color 0.2s;
        }
        nav a:hover { color: #7dd3fc; }

        /* -- Hero -- */
        .hero {
            text-align: center;
            padding: 100px 24px 80px;
            max-width: 780px;
            margin: 0 auto;
        }
        .hero .badge {
            display: inline-block;
            background: #1e293b;
            border: 1px solid #334155;
            color: #7dd3fc;
            font-size: 0.82rem;
            padding: 6px 14px;
            border-radius: 20px;
            margin-bottom: 24px;
            letter-spacing: 0.04em;
        }
        .hero h1 {
            font-size: 3.2rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 12px;
            line-height: 1.2;
        }
        .hero h1 span { color: #7dd3fc; }
        .hero .subtitle {
            font-size: 1.15rem;
            color: #94a3b8;
            margin-bottom: 8px;
        }
        .hero .location {
            color: #64748b;
            font-size: 0.92rem;
            margin-bottom: 32px;
        }
        .hero .cta-row {
            display: flex;
            justify-content: center;
            gap: 14px;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-block;
            padding: 10px 22px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            transition: transform 0.15s, box-shadow 0.15s;
        }
        .btn:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,0.3); }
        .btn-primary { background: #7dd3fc; color: #0f172a; }
        .btn-outline { border: 1px solid #334155; color: #cbd5e1; }

        /* -- Section shared -- */
        section { padding: 72px 24px; max-width: 900px; margin: 0 auto; }
        .section-title { font-size: 1.6rem; color: #f1f5f9; margin-bottom: 8px; }
        .section-sub { color: #64748b; font-size: 0.95rem; margin-bottom: 40px; }
        .divider {
            width: 44px; height: 3px;
            background: #7dd3fc;
            border-radius: 2px;
            margin-bottom: 12px;
        }

        /* -- Stats -- */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 56px;
        }
        .stat-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 28px 16px;
            text-align: center;
        }
        .stat-card .num {
            font-size: 2rem;
            font-weight: 700;
            color: #7dd3fc;
        }
        .stat-card .label {
            font-size: 0.82rem;
            color: #64748b;
            margin-top: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* -- About -- */
        .about-text {
            color: #cbd5e1;
            font-size: 1.02rem;
            max-width: 720px;
        }
        .about-text p { margin-bottom: 16px; }
        .about-text strong { color: #f1f5f9; }

        /* -- Skills -- */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
        }
        .skill-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 24px;
        }
        .skill-card h4 {
            color: #7dd3fc;
            font-size: 0.88rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 14px;
        }
        .tag-row { display: flex; flex-wrap: wrap; gap: 8px; }
        .tag {
            background: #0f172a;
            border: 1px solid #334155;
            color: #94a3b8;
            font-size: 0.8rem;
            padding: 4px 10px;
            border-radius: 6px;
        }

        /* -- Projects -- */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
        }
        .project-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 24px;
            text-decoration: none;
            color: inherit;
            transition: border-color 0.2s;
            display: block;
        }
        .project-card:hover { border-color: #7dd3fc; }
        .project-card h4 { color: #f1f5f9; margin-bottom: 6px; font-size: 1rem; }
        .project-card p { color: #64748b; font-size: 0.88rem; margin-bottom: 10px; }
        .project-card .stars { color: #7dd3fc; font-size: 0.82rem; }

        /* -- Content / Writing -- */
        .writing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
        }
        .writing-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 24px;
            text-decoration: none;
            color: inherit;
            transition: border-color 0.2s;
            display: block;
        }
        .writing-card:hover { border-color: #7dd3fc; }
        .writing-card .platform-badge {
            display: inline-block;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #7dd3fc;
            margin-bottom: 10px;
        }
        .writing-card h4 { color: #f1f5f9; font-size: 0.95rem; margin-bottom: 6px; }
        .writing-card p { color: #64748b; font-size: 0.85rem; }

        /* -- Connect -- */
        .connect-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px;
        }
        .connect-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 18px 16px;
            text-decoration: none;
            color: #cbd5e1;
            font-size: 0.88rem;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: border-color 0.2s, background 0.2s;
        }
        .connect-card:hover { border-color: #7dd3fc; background: #253347; }
        .connect-card .icon { font-size: 1.2rem; }

        /* -- Footer -- */
        footer {
            text-align: center;
            padding: 48px 24px;
            border-top: 1px solid #1e293b;
            color: #475569;
            font-size: 0.85rem;
        }
        footer a { color: #7dd3fc; text-decoration: none; }

        /* -- Responsive -- */
        @media (max-width: 600px) {
            .hero h1 { font-size: 2.2rem; }
            nav ul { gap: 18px; }
        }
    </style>
</head>
<body>

<nav>
    <ul>
        <li><a href="#about">About</a></li>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#projects">Projects</a></li>
        <li><a href="#writing">Writing</a></li>
        <li><a href="#connect">Connect</a></li>
    </ul>
</nav>

<header class="hero">
    <div class="badge">&#9679; ML Engineer @ Accenture</div>
    <h1>Aditya <span>Shrivastava</span></h1>
    <p class="subtitle">Machine Learning & NLP Engineer | LLM Enthusiast</p>
    <p class="location">Bengaluru, India &nbsp;&#8226;&nbsp; AI/ML Diploma, University of Hyderabad</p>
    <div class="cta-row">
        <a href="#connect" class="btn btn-primary">Connect</a>
        <a href="#projects" class="btn btn-outline">Case Studies</a>
        <a href="#about" class="btn btn-outline">About</a>
    </div>
</header>

<section>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="num">4+ yrs</div>
            <div class="label">ML Engineering</div>
        </div>
        <div class="stat-card">
            <div class="num">30% faster</div>
            <div class="label">Problem Resolution</div>
        </div>
        <div class="stat-card">
            <div class="num">PICS</div>
            <div class="label">Patent Evaluation</div>
        </div>
        <div class="stat-card">
            <div class="num">639+</div>
            <div class="label">Community Followers</div>
        </div>
    </div>
</section>

<section id="about">
    <div class="divider"></div>
    <h2 class="section-title">About Me</h2>
    <p class="section-sub">AI-driven reliability and operations</p>
    <div class="about-text">
        <p>
            At <strong>Accenture</strong> I design and productionize ML systems that predict sensor failures. By
            tightening data validation, crafting high-signal features, and testing models from logistic regression
            through gradient boosting, I raised accuracy and trust in critical monitoring pipelines.
        </p>
        <p>
            Earlier at <strong>Cerner</strong> I built a Python-based NLP solution that cut problem resolution time
            by <strong>30%</strong>. The POC, <strong>PICS (Problem Identification through Contextual Search)</strong>,
            is integrated into Cerner's analytics platform <strong>MyJarvis</strong> and is under patent evaluation.
        </p>
        <p>
            I care about operational excellence: clear documentation, disciplined train/validation/test splits,
            continuous performance monitoring, and close collaboration with domain experts to keep models aligned to
            business outcomes.
        </p>
    </div>
</section>

<section id="skills">
    <div class="divider"></div>
    <h2 class="section-title">Skills &amp; Tools</h2>
    <p class="section-sub">What I use to ship reliable ML</p>
    <div class="skills-grid">
        <div class="skill-card">
            <h4>Machine Learning</h4>
            <div class="tag-row">
                <span class="tag">Logistic Regression</span>
                <span class="tag">Decision Trees</span>
                <span class="tag">Random Forests</span>
                <span class="tag">Gradient Boosting</span>
            </div>
        </div>
        <div class="skill-card">
            <h4>NLP &amp; GenAI</h4>
            <div class="tag-row">
                <span class="tag">NLP</span>
                <span class="tag">Text Classification</span>
                <span class="tag">LLMs</span>
                <span class="tag">Text2SQL</span>
                <span class="tag">Generative AI</span>
            </div>
        </div>
        <div class="skill-card">
            <h4>Data Quality</h4>
            <div class="tag-row">
                <span class="tag">Data Validation</span>
                <span class="tag">Outlier Handling</span>
                <span class="tag">Feature Selection</span>
                <span class="tag">Feature Extraction</span>
                <span class="tag">Train/Val/Test</span>
            </div>
        </div>
        <div class="skill-card">
            <h4>Platforms &amp; Tools</h4>
            <div class="tag-row">
                <span class="tag">Python</span>
                <span class="tag">SQL</span>
                <span class="tag">Elasticsearch (Lucene)</span>
                <span class="tag">Remedy Index</span>
                <span class="tag">PowerShell</span>
            </div>
        </div>
        <div class="skill-card">
            <h4>MLOps &amp; Evaluation</h4>
            <div class="tag-row">
                <span class="tag">Performance Monitoring</span>
                <span class="tag">Model Evaluation</span>
                <span class="tag">Documentation</span>
                <span class="tag">Reproducibility</span>
            </div>
        </div>
        <div class="skill-card">
            <h4>Operations</h4>
            <div class="tag-row">
                <span class="tag">Incident Response</span>
                <span class="tag">Root Cause Analysis</span>
                <span class="tag">Stakeholder Comms</span>
                <span class="tag">Automation</span>
            </div>
        </div>
    </div>
</section>

<section id="projects">
    <div class="divider"></div>
    <h2 class="section-title">Case Studies</h2>
    <p class="section-sub">Selected work from Accenture and Cerner</p>
    <div class="projects-grid">
        <a href="#!" class="project-card">
            <h4>Sensor Failure Prediction</h4>
            <p>Built robust validation, feature engineering, and ensemble models to forecast sensor outages with higher accuracy.</p>
            <span class="stars">Accenture</span>
        </a>
        <a href="#!" class="project-card">
            <h4>PICS for MyJarvis</h4>
            <p>Python NLP pipeline that identifies ticket trends, cutting TAT by 30%; integrated into Cerner's analytics stack.</p>
            <span class="stars">Patent Evaluation</span>
        </a>
        <a href="#!" class="project-card">
            <h4>Server Health Automation</h4>
            <p>Automated health checks and incident playbooks, improving response times for critical systems.</p>
            <span class="stars">Operations</span>
        </a>
        <a href="#!" class="project-card">
            <h4>Text2SQL Experiments</h4>
            <p>Explorations in translating natural language into SQL to accelerate analytics for stakeholders.</p>
            <span class="stars">Research</span>
        </a>
    </div>
</section>

<section id="writing">
    <div class="divider"></div>
    <h2 class="section-title">Writing &amp; Highlights</h2>
    <p class="section-sub">Sharing learnings with the community</p>
    <div class="writing-grid">
        <a href="#connect" class="writing-card">
            <div class="platform-badge">LinkedIn &middot; 639+ Followers</div>
            <h4>AI/ML Practice Notes</h4>
            <p>Posts on model evaluation, data quality, and operationalizing ML systems.</p>
        </a>
        <a href="#projects" class="writing-card">
            <div class="platform-badge">Cerner &middot; MyJarvis</div>
            <h4>PICS Patent Journey</h4>
            <p>Documenting lessons from taking an NLP POC into production and patent review.</p>
        </a>
        <a href="#projects" class="writing-card">
            <div class="platform-badge">#Text2SQL</div>
            <h4>Querying with Natural Language</h4>
            <p>Experiments and commentary on bridging human questions to structured data retrieval.</p>
        </a>
    </div>
</section>

<section id="connect">
    <div class="divider"></div>
    <h2 class="section-title">Connect</h2>
    <p class="section-sub">Links to reach Aditya (replace with your URLs)</p>
    <div class="connect-grid">
        <a href="#!" class="connect-card">
            <span class="icon">&#128188;</span> LinkedIn
        </a>
        <a href="#!" class="connect-card">
            <span class="icon">&#128196;</span> GitHub / Projects
        </a>
        <a href="#!" class="connect-card">
            <span class="icon">&#128231;</span> Email
        </a>
        <a href="#!" class="connect-card">
            <span class="icon">&#128214;</span> Resume
        </a>
        <a href="#!" class="connect-card">
            <span class="icon">&#128227;</span> X / Twitter
        </a>
        <a href="#!" class="connect-card">
            <span class="icon">&#128197;</span> Book a Call
        </a>
        <a href="#!" class="connect-card">
            <span class="icon">&#127891;</span> Certifications
        </a>
        <a href="#!" class="connect-card">
            <span class="icon">&#128196;</span> Case Studies
        </a>
    </div>
</section>

<footer>
    <p>&copy; 2026 Aditya Shrivastava &middot; Built with Flask &amp; Python</p>
</footer>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
