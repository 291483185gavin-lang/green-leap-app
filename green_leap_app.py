import streamlit as st
import pandas as pd
import numpy as np
import random
from collections import Counter
import base64
from io import BytesIO
from datetime import datetime

# -----------------------------
# 🌿 Part 1: 基础设置
# -----------------------------
st.set_page_config(page_title="Green Leap", page_icon="🌱", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "welcome"
    # ✅ Navigation Helper Function
def go_to(page_name: str):
    """
    A reliable page navigation function for Streamlit.
    Ensures the session updates before rerun.
    """
    import streamlit as st
    st.session_state.page = page_name
    st.experimental_rerun()


# -----------------------------
# 🌿 Part 2: 模拟假数据（升级版，带完整岗位详情）
# -----------------------------
roles = [
    "Sustainability Analyst", "Green Data Engineer", "ESG Specialist", "Urban Planner",
    "Carbon Accountant", "Renewable Energy Technician", "Climate Policy Intern",
    "Environmental Scientist", "Circular Economy Researcher", "Sustainable Finance Officer"
]

companies = [
    "EcoFuture Labs", "Blue Earth Partners", "ReLeaf Consulting", "GreenMind Analytics",
    "SolarEdge Asia", "NatureWorks", "Future Planet", "CleanCity Labs", "ZeroWaste Hub", "GreenLeap Youth Network"
]

categories = [
    "Renewable Energy", "Urban Planning", "Climate Strategy", "Circular Economy",
    "Green Finance", "Biodiversity", "Sustainable Agriculture", "Smart Mobility"
]

skills = [
    "Python", "Data Analysis", "Carbon Accounting", "Sustainability Reporting", 
    "Machine Learning", "Stakeholder Engagement", "ESG Metrics", "Life Cycle Assessment",
    "GIS Mapping", "Project Management"
]

cities = ["Singapore", "Jakarta", "Manila", "Kuala Lumpur", "Bangkok", "Hanoi", "Tokyo", "Seoul"]

apprenticeship_programs = [
    "Youth Climate Fellowship", "Green Apprenticeship Pathway", "Circular Economy Starter",
    "Sustainability Data Bootcamp", "Renewable Energy Trainee Program"
]

career_paths = [
    "Apprentice → Sustainability Analyst → ESG Manager → Sustainability Director",
    "Intern → Research Assistant → Project Coordinator → Climate Policy Lead",
    "Data Assistant → Analyst → Sustainability Strategist → Regional Director"
]

training_links = [
    "https://www.coursera.org/learn/sustainability-reporting",
    "https://www.edx.org/course/sustainable-finance",
    "https://www.futurelearn.com/courses/climate-change-leadership"
]

support_programs = [
    "Youth Green Mentorship", "UN SDG Internship", "Community Climate Lab", 
    "ASEAN Green Skills Accelerator", "EcoCampus Partnership"
]

descriptions = [
    "Assist companies in implementing carbon accounting systems and climate disclosure frameworks.",
    "Support renewable energy data modeling and energy efficiency tracking projects.",
    "Collaborate with government and NGOs on urban sustainability planning and green infrastructure.",
    "Work with teams to design strategies for circular economy transitions and waste reduction.",
    "Conduct ESG data analytics and support sustainability reporting to international standards."
]

data = []
for _ in range(150):
    data.append({
        "Role": random.choice(roles),
        "Company": random.choice(companies),
        "Category": random.choice(categories),
        "City": random.choice(cities),
        "KeySkills": ", ".join(random.sample(skills, 3)),
        "MatchScore": random.randint(60, 100),
        "SalaryRange": random.choice(["USD 700–1000/month", "USD 1000–1500/month", "USD 1500–2000/month"]),
        "CareerPath": random.choice(career_paths),
        "SupportPrograms": random.choice(support_programs),
        "Apprenticeship": random.choice(apprenticeship_programs),
        "TrainingLink": random.choice(training_links),
        "JobDescription": random.choice(descriptions)
    })

jobs_df = pd.DataFrame(data)


# -----------------------------
# 🌿 Part 3: 欢迎页
# -----------------------------
if st.session_state.page == "welcome":
    st.markdown("""
        <div style='text-align:center; padding:80px 0; background:linear-gradient(to bottom, #edf8ef, white); border-radius:20px'>
            <h1 style='color:#2E8B57; font-size:48px;'>🌱 Green Leap</h1>
            <h3 style='color:#3c8c60;'>Empowering your leap into sustainable futures</h3>
            <p style='color:gray;'>Your personal guide to the future of green careers</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Exploring", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

# -----------------------------
# 🌿 Part 4: 主菜单逻辑
# -----------------------------
if st.session_state.page == "main":
    with st.sidebar:
        st.title("📋 Main Menu")
        section = st.radio(
            "Choose a section:",
            [
                "Find Green Jobs",
                "Match My Skills",
                "30/60/90 Path",
                "Smart Summary",
                "Green Coach Chat",
                "Dashboard",
                "Green Economy Reality"
            ]
        )

            # -----------------------------
    # Section 1: Find Green Jobs (Dropdown City + Smart Search)
    # -----------------------------
    if section == "Find Green Jobs":
        import math, random, difflib

        # --- Header ---
        st.markdown("""
        <div style='text-align:center; padding:25px; background:linear-gradient(to right, #e8f5e9, #ffffff); border-radius:15px;'>
            <h2 style='color:#2E8B57; font-size:36px;'>🌿 Find Your Green Career Path</h2>
            <p style='color:#4f6d54; font-size:16px;'>Empowering Southeast Asian youth to explore accessible, meaningful, and growth-oriented sustainable jobs.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        # --- City Dropdown ---
        cities = ["All", "Singapore", "Jakarta", "Bangkok", "Manila", "Kuala Lumpur", "Seoul", "Tokyo", "Sydney"]
        col1, col2 = st.columns([1.2, 2.8])
        with col1:
            city = st.selectbox("🏙️ Select City", cities)
        with col2:
            keyword = st.text_input("🔎 Search by Role, Skill, or Company", placeholder="e.g., Energy, Data, ESG...")

        # --- Fuzzy Match Helper ---
        def fuzzy_match(query, text_list):
            matches = difflib.get_close_matches(query.lower(), [t.lower() for t in text_list], n=10, cutoff=0.3)
            return [t for t in text_list if t.lower() in matches]

        # --- Filter Logic ---
        filtered_jobs = jobs_df.copy()

        # City Filter
        if city != "All":
            filtered_jobs = filtered_jobs[filtered_jobs["City"].str.contains(city, case=False, na=False)]

        # Fuzzy Keyword Filter
        if keyword.strip():
            matched_roles = fuzzy_match(keyword, filtered_jobs["Role"].tolist())
            matched_categories = fuzzy_match(keyword, filtered_jobs["Category"].tolist())
            matched_companies = fuzzy_match(keyword, filtered_jobs["Company"].tolist())
            matched_skills = fuzzy_match(keyword, [", ".join(sk.split(",")) for sk in filtered_jobs["KeySkills"].tolist()])

            filtered_jobs = filtered_jobs[
                filtered_jobs["Role"].isin(matched_roles)
                | filtered_jobs["Category"].isin(matched_categories)
                | filtered_jobs["Company"].isin(matched_companies)
                | filtered_jobs["KeySkills"].isin(matched_skills)
            ]

        # --- No Results → Random Suggestion ---
        if len(filtered_jobs) == 0:
            st.warning("⚠️ No exact matches found. Here are 10 suggested opportunities you might like:")
            filtered_jobs = jobs_df.sample(10)

        total_jobs = len(filtered_jobs)

        # --- Summary metrics ---
        st.markdown("### 🌱 Market Snapshot")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total Opportunities", total_jobs)
        col_b.metric("Average Match Score", round(filtered_jobs["MatchScore"].mean(), 2) if total_jobs > 0 else "—")
        col_c.metric("Active Cities", filtered_jobs["City"].nunique() if total_jobs > 0 else "—")

        st.markdown("<hr style='margin-top:10px;margin-bottom:10px;'>", unsafe_allow_html=True)

        # --- View Mode Switch ---
        if "view_all" not in st.session_state:
            st.session_state.view_all = False

        # --- Helper: Random Career Stage ---
        def random_stage():
            return random.choice(["Entry Level", "Mid Career", "Advanced"])

        # --- Style Helper for Tag ---
        def stage_style(stage):
            color = {"Entry Level": "#66bb6a", "Mid Career": "#43a047", "Advanced": "#1b5e20"}[stage]
            return f"background:{color}; color:white; padding:4px 10px; border-radius:10px; font-size:12px; font-weight:bold;"

        # --- Pagination (works for both modes) ---
        jobs_per_page = 10
        total_pages = math.ceil(len(filtered_jobs) / jobs_per_page)
        page = st.number_input("Page", min_value=1, max_value=max(total_pages, 1), value=1, step=1)

        start_idx = (page - 1) * jobs_per_page
        end_idx = start_idx + jobs_per_page
        page_jobs = filtered_jobs.iloc[start_idx:end_idx]

        # --- Job Cards Display ---
        for _, row in page_jobs.iterrows():
            stage = random_stage()
            icon = "🌱"
            if "Engineer" in row.Role: icon = "⚙️"
            elif "Analyst" in row.Role: icon = "📊"
            elif "Manager" in row.Role: icon = "🧭"
            elif "Research" in row.Role: icon = "🔬"
            elif "Consultant" in row.Role: icon = "🤝"

            st.markdown(f"""
            <div style='background:#f9fff9; border:1px solid #cdeccd; border-radius:15px; padding:22px; margin-bottom:18px;
                        box-shadow:0 4px 10px rgba(0,0,0,0.06); display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'>
                    <h3 style='color:#1b4332; margin-bottom:6px;'>{icon} {row.Role}</h3>
                    <p style='margin:0; font-size:15px; color:#2f4f4f;'><b>🏢 Company:</b> {row.Company}</p>
                    <p style='margin:0; font-size:15px; color:#2f4f4f;'><b>📍 City:</b> {row.City} <b>💼 Category:</b> {row.Category}</p>
                    <p style='margin:0; font-size:14px; color:#406040;'><b>🎯 Key Skills:</b> {row.KeySkills}</p>
                    <progress value='{row.MatchScore}' max='100' style='width:100%; height:12px;'></progress>
                </div>
                <div style='margin-left:15px;'>
                    <span style='{stage_style(stage)}'>{stage}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📘 View Full Job Details"):
                st.markdown(f"""
                <div style='font-size:14px; color:#1c1c1c;'>
                    <p><b>💡 Job Description:</b><br>{row.JobDescription}</p>
                    <p><b>💰 Salary Range:</b> {row.SalaryRange}</p>
                    <p><b>📈 Career Path:</b><br>{row.CareerPath}</p>
                    <p><b>🧭 Apprenticeship Program:</b> {row.Apprenticeship}</p>
                    <p><b>🤝 Support Programs:</b> {row.SupportPrograms}</p>
                </div>
                """, unsafe_allow_html=True)

      
        # --- Context Section ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:#e8f5e9; padding:18px; border-radius:12px; border-left:5px solid #2E8B57;'>
        <h4 style='color:#2E8B57;'>🌍 Why This Matters</h4>
        <p style='color:#3e5e4e;'>
        By making green jobs visible, guided, and aspirational, this platform helps Southeast Asian youth access real sustainable pathways.  
        Even if they start small — through apprenticeships or short-term training — each step makes sustainability an achievable career reality. 🌱
        </p>
        </div>
        """, unsafe_allow_html=True)

        # -----------------------------
        # 🧠 AI Recommendation Section
        # -----------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🤖 AI Recommendation")

        # Build the context
        city_context = f"in {city}" if city != "All" else "across Asia-Pacific"
        keyword_context = keyword if keyword.strip() else "sustainability careers"

        # Generate contextual recommendation
        ai_reco = f"""
        <div style='background:#f0f9f4; padding:20px; border-radius:15px; border-left:5px solid #2E8B57;
                    box-shadow:0 3px 8px rgba(0,0,0,0.05);'>
        <h4 style='color:#2E8B57;'>💬 Recommended Focus Area</h4>
        <p style='color:#2f4f4f; font-size:15px;'>
        Based on your interest in <b>{keyword_context}</b> {city_context}, 
        we suggest exploring emerging green roles that emphasize <b>applied sustainability, 
        renewable innovation, and social impact design</b>.
        </p>
        <p style='color:#3e5e4e; font-size:14px;'>
        These areas are expanding rapidly in Southeast Asia, particularly within renewable energy, 
        smart mobility, and sustainable finance. Entry-level professionals can begin through 
        apprenticeship programs or data-focused analytical roles before advancing toward 
        project management or sustainability consulting positions.
        </p>
        <p style='color:#3c6e47; font-size:14px;'>
        🌿 In short: your chosen path combines <b>personal impact</b> with <b>career resilience</b> — 
        key drivers for the next generation of climate innovators.
        </p>
        </div>
        """
        st.markdown(ai_reco, unsafe_allow_html=True)


            # -----------------------------
    # Section 2: Match My Skills (Optimized Stable Version)
    # -----------------------------
    elif section == "Match My Skills":
        import random

        st.markdown("""
        <div style='text-align:center; padding:25px; background:linear-gradient(to right, #e8f5e9, #ffffff); border-radius:15px;'>
            <h2 style='color:#2E8B57; font-size:32px;'>🧠 Match My Skills</h2>
            <p style='color:#4f6d54; font-size:15px;'>Discover how your unique abilities align with sustainable career opportunities.</p>
        </div>
        """, unsafe_allow_html=True)        

        # --- 1️⃣ 预设技能池 ---
        skill_pool = [
            "Data Analysis", "Public Speaking", "Renewable Energy", "Climate Literacy", "Project Management",
            "Communication", "Creativity", "Social Media", "Leadership", "Research", "ESG Reporting", "Carbon Accounting",
            "Graphic Design", "Engineering", "Problem Solving", "Community Engagement", "AI & Technology",
            "Sustainable Finance", "Circular Economy", "Environmental Awareness"
        ]

        selected_skills = st.multiselect("🎯 Choose your skills:", skill_pool)

        if not selected_skills:
            st.info("💡 Please select at least one skill to continue.")
            st.stop()

        # --- 2️⃣ 熟练度等级 ---
        st.markdown("### ⚙️ Rate Your Skill Proficiency")
        levels = ["Beginner", "Intermediate", "Advanced", "Expert"]
        user_levels = {}
        for skill in selected_skills:
            user_levels[skill] = st.select_slider(f"{skill} proficiency level:", options=levels)

        # --- 3️⃣ 自动计算 Green Readiness Score ---
        avg_level_index = sum(levels.index(v) for v in user_levels.values()) / len(user_levels)
        readiness_score = int((avg_level_index + 1) * 25)
        if readiness_score < 40:
            career_stage = "Entry Level"
        elif readiness_score < 70:
            career_stage = "Mid Career"
        else:
            career_stage = "Advanced Stage"

        st.markdown(f"<h4 style='color:#2E8B57;'>🌿 Green Readiness Score: {readiness_score}/100</h4>", unsafe_allow_html=True)
        st.progress(readiness_score / 100)
        st.caption(f"Current Stage: **{career_stage}** — Keep growing your sustainable skillset!")

        # --- 4️⃣ 匹配职业数据库 ---
        job_database = [
            {"Role": "ESG Analyst", "Skills": ["Data Analysis", "ESG Reporting", "Carbon Accounting"], "Stage": "Mid Career"},
            {"Role": "Sustainability Consultant", "Skills": ["Project Management", "Climate Literacy", "Leadership"], "Stage": "Advanced Stage"},
            {"Role": "Community Engagement Officer", "Skills": ["Communication", "Public Speaking", "Community Engagement"], "Stage": "Entry Level"},
            {"Role": "Green Data Analyst", "Skills": ["Data Analysis", "AI & Technology", "Sustainable Finance"], "Stage": "Mid Career"},
            {"Role": "Renewable Engineer", "Skills": ["Engineering", "Renewable Energy", "Problem Solving"], "Stage": "Advanced Stage"},
            {"Role": "Climate Policy Assistant", "Skills": ["Research", "Environmental Awareness", "Climate Literacy"], "Stage": "Entry Level"},
            {"Role": "Eco Marketing Specialist", "Skills": ["Creativity", "Social Media", "Communication"], "Stage": "Mid Career"},
            {"Role": "Circular Economy Coordinator", "Skills": ["Circular Economy", "Project Management", "Problem Solving"], "Stage": "Mid Career"},
            {"Role": "Sustainable Finance Advisor", "Skills": ["Sustainable Finance", "Leadership", "Data Analysis"], "Stage": "Advanced Stage"}
        ]

        def match_score(job):
            overlap = len(set(selected_skills) & set(job["Skills"]))
            return overlap

        ranked_jobs = sorted(job_database, key=match_score, reverse=True)[:5]

        st.markdown("### 💼 Recommended Green Career Matches")
        for job in ranked_jobs:
            overlap = set(selected_skills) & set(job["Skills"])
            missing = set(job["Skills"]) - set(selected_skills)
            st.markdown(f"""
            <div style='background:#ffffff; border:1px solid #d8f3dc; border-radius:12px; padding:14px; margin:10px 0; box-shadow:1px 2px 5px rgba(0,0,0,0.05);'>
                <div style='display:flex; justify-content:space-between;'>
                    <h4 style='color:#2E8B57;'>🌱 {job['Role']}</h4>
                    <span style='color:#4f6d54; font-size:13px;'>{job['Stage']}</span>
                </div>
                <p style='font-size:14px; color:#333333; margin-top:5px;'>
                Matched Skills: <b>{', '.join(overlap) if overlap else 'N/A'}</b><br>
                Missing Skills: <b>{', '.join(missing) if missing else 'None'}</b>
                </p>
                <p style='color:#2E8B57; font-size:13px; margin-top:6px;'>💡 This role contributes to SDG13 & SDG8.</p>
            </div>
            """, unsafe_allow_html=True)

        # --- 5️⃣ 缺失技能总结 + 建议 ---
        missing_all = set()
        for job in ranked_jobs:
            missing_all.update(set(job["Skills"]) - set(selected_skills))

        st.markdown("### 🧩 Skill Gaps & Next Steps")
        if missing_all:
            st.warning(f"To progress further, consider developing: {', '.join(missing_all)}")
            st.info("🎓 Try exploring short courses, mentorship programs, or Green Apprenticeships to close these gaps.")
        else:
            st.success("🌟 Excellent! You have strong alignment with multiple green career paths.")
        
        # -----------------------------
        # 📊 Compare with Market Demand (Smart Filtered + Expandable)
        # -----------------------------
        st.markdown("---")
        st.markdown("### 📊 Compare with Market Demand")
        st.caption("Discover how your selected skills compare with the most in-demand green job skills across Asia-Pacific.")

        # 固定技能热度榜
        skill_popularity = {
            "Data Analysis": 95,
            "Project Management": 88,
            "Sustainable Finance": 83,
            "AI & Technology": 80,
            "Climate Literacy": 78,
            "Communication": 75,
            "Leadership": 72,
            "Renewable Energy": 70,
            "Circular Economy": 68,
            "Community Engagement": 65
        }

        # -----------------------------
        # 智能展示逻辑
        # -----------------------------
        matched_skills = [s for s in selected_skills if s in skill_popularity]
        if matched_skills:
            display_list = [(s, skill_popularity[s]) for s in matched_skills]
            st.markdown("#### 🌱 Skills You Already Have (Ranked by Market Demand)")
        else:
            display_list = list(skill_popularity.items())[:3]
            st.markdown("#### 🌱 Top 3 Most In-Demand Sustainability Skills")

        for skill, score in display_list:
            heat_level = (
                "🔥 High Demand" if score >= 85 else
                "🌿 Medium Demand" if score >= 75 else
                "🌾 Emerging Skill"
            )
            match = "✅ You already have this skill" if skill in selected_skills else "✨ Highly Recommended to Learn"
            color = "#2E8B57" if skill in selected_skills else "#b7e4c7"

            st.markdown(
                f"""
                <div style='background-color:#f8fff9; border-left:6px solid {color};
                            border-radius:10px; padding:10px 15px; margin-bottom:10px;'>
                    <h5 style='color:{color}; margin-bottom:4px;'>{skill}</h5>
                    <p style='margin:0; color:gray;'>{heat_level} • Popularity Index: {score}</p>
                    <div style='height:8px; width:{score}%; background-color:{color}; border-radius:4px; margin:6px 0;'></div>
                    <p style='margin:0; color:#444;'>{match}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 折叠完整榜单
        with st.expander("📈 View Full Market Ranking"):
            for skill, score in skill_popularity.items():
                heat_level = (
                    "🔥 High Demand" if score >= 85 else
                    "🌿 Medium Demand" if score >= 75 else
                    "🌾 Emerging Skill"
                )
                match = "✅ You already have this skill" if skill in selected_skills else "✨ Not in your skillset"
                color = "#2E8B57" if skill in selected_skills else "#b7e4c7"
                st.markdown(
                    f"""
                    <div style='background-color:#f8fff9; border-left:6px solid {color};
                                border-radius:10px; padding:10px 15px; margin-bottom:8px;'>
                        <h6 style='color:{color}; margin-bottom:3px;'>{skill}</h6>
                        <p style='margin:0; color:gray;'>{heat_level} • Popularity Index: {score}</p>
                        <div style='height:6px; width:{score}%; background-color:{color}; border-radius:4px; margin:4px 0;'></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -----------------------------
        # 💡 Insight Summary
        # -----------------------------
        st.markdown("### 💡 Insight Summary")

        top_user_skills = [s for s in selected_skills if s in skill_popularity.keys()]
        if top_user_skills:
            top_text = ", ".join(top_user_skills[:3])
            score = round(len(top_user_skills) / len(skill_popularity) * 100)
            st.success(
                f"Your selected skills ({top_text}) align with {score}% of the most in-demand sustainability skills. "
                "You're already positioned for strong career potential in green innovation and ESG transformation."
            )
        else:
            st.info(
                "Your current skillset doesn’t overlap with top sustainability capabilities yet. "
                "Start by developing Data Analysis, Project Management, or Climate Literacy to enter this fast-growing field."
            )

        # -----------------------------
        # 🌍 Overall Skill Fit
        # -----------------------------
        st.markdown("### 🌍 Overall Skill Alignment")
        alignment = round(len(top_user_skills) / len(skill_popularity) * 100) if top_user_skills else 20
        st.progress(alignment / 100)
        st.caption(f"Overall Market Fit: {alignment}%")


                            # -----------------------------
    # 🎯 Section: 30/60/90 Career Path (Full Multi-Skill Version)
    # -----------------------------
    elif section == "30/60/90 Path":
        import random

        st.markdown("<h2 style='color:#2E8B57;'>🎯 AI-Powered 30/60/90 Career Growth Pathway</h2>", unsafe_allow_html=True)
        st.caption("Each selected skill generates a structured 3-phase development plan designed for Southeast Asian youth entering green careers.")
        st.divider()

        # Step 1: 选择技能
        st.markdown("### 🧩 Step 1. Select up to Two Skills to Build On")
        selected_skills = st.multiselect(
            "Choose your key sustainability skills (max 2):",
            [
                "Data Analysis", "Carbon Accounting", "Renewable Energy", "AI for Sustainability",
                "Circular Design", "Smart Mobility", "Project Management",
                "Behavioral Change Design", "Sustainable Finance", "Environmental Policy"
            ],
            max_selections=2
        )

        proficiency = st.select_slider(
            "Select your current proficiency level:",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )

        st.markdown("<p style='color:gray; font-style:italic;'>💡 Mastery grows from focus — select one or two skills to specialize in, and commit to consistency.</p>", unsafe_allow_html=True)

        # Step 2: 生成成长路径
        if st.button("✨ Generate My 30/60/90 Growth Plan", use_container_width=True):
            if not selected_skills:
                st.warning("Please select at least one skill to continue.")
            else:
                st.markdown("---")
                st.markdown("### 🌱 Your Personalized AI-Generated Learning Roadmap")

                # 各技能完整内容
                plans = {
                    "Data Analysis": {
                        "30": """
                        <b>First 30 Days — Build Data Awareness</b><br><br>
                        Begin with foundational tools like Excel and Python to clean and organize sustainability datasets.  
                        Focus on real environmental metrics such as carbon emissions, waste data, or water consumption trends.  
                        Use online open resources like UNEP and “Our World in Data” to develop confidence reading complex datasets.  
                        Your goal is not to master code yet, but to start thinking in terms of data-driven questions.
                        """,
                        "60": """
                        <b>Next 60 Days — Apply Analytical Thinking</b><br><br>
                        Learn how to visualize patterns and extract insights.  
                        Build interactive dashboards using Power BI or Tableau to track renewable adoption or plastic waste flows.  
                        Join a Kaggle competition or a community hackathon to test your skills.  
                        This period transforms you from a learner into a practical data storyteller.
                        """,
                        "90": """
                        <b>Final 90 Days — Translate Data into Action</b><br><br>
                        Combine technical and communication skills.  
                        Write a short sustainability report using your visualizations, focusing on a country or company’s progress.  
                        Present your findings on social media or in a small group.  
                        You now possess a concrete data portfolio demonstrating analytical and impact-driven capabilities.
                        """
                    },

                    "Carbon Accounting": {
                        "30": """
                        <b>First 30 Days — Understand the Carbon System</b><br><br>
                        Study the GHG Protocol, ISO 14064, and ESG concepts.  
                        Focus on how organizations quantify emissions in Scope 1, 2, and 3.  
                        Build small exercises: estimate your own footprint using online calculators.  
                        Begin to appreciate the link between measurement and corporate responsibility.
                        """,
                        "60": """
                        <b>Next 60 Days — Learn Reporting Practices</b><br><br>
                        Use mock company data to create carbon emission tables.  
                        Practice using Excel to calculate reduction baselines.  
                        Study how reports align with frameworks like CDP or TCFD.  
                        Reflect on ethical implications — how transparency builds trust in sustainable business.
                        """,
                        "90": """
                        <b>Final 90 Days — Build a Showcase Portfolio</b><br><br>
                        Create a simplified carbon audit for a company or school.  
                        Include visualization of results and proposed mitigation strategies.  
                        You’ll finish with a portfolio that signals readiness for ESG and carbon management roles.
                        """
                    },

                    "Renewable Energy": {
                        "30": """
                        <b>First 30 Days — Explore the Energy Transition</b><br><br>
                        Learn the science behind solar PV, wind turbines, and hydro systems.  
                        Use interactive online tools like PVWatts to simulate energy production.  
                        Read regional renewable adoption reports from ASEAN and IRENA.  
                        Understand energy efficiency as a bridge between climate goals and real solutions.
                        """,
                        "60": """
                        <b>Next 60 Days — Build Applied Knowledge</b><br><br>
                        Work on a simple renewable project — calculate payback period for solar installation or efficiency gains in lighting.  
                        Understand how policy incentives (feed-in tariffs, subsidies) drive market demand.  
                        Network with sustainability forums to connect theory and application.
                        """,
                        "90": """
                        <b>Final 90 Days — Create Your Renewable Case</b><br><br>
                        Write a case study analyzing a successful clean energy transition.  
                        Include both economic and social perspectives.  
                        Present your project in class or online — demonstrating both technical and storytelling skills.
                        """
                    },

                    "AI for Sustainability": {
                        "30": """
                        <b>First 30 Days — Learn AI Fundamentals</b><br><br>
                        Study how AI models support environmental monitoring, such as deforestation detection and emission tracking.  
                        Learn Python basics and machine learning concepts.  
                        Focus on environmental data applications, not complex coding yet.  
                        You’re setting a foundation to connect AI logic with sustainability challenges.
                        """,
                        "60": """
                        <b>Next 60 Days — Start Building</b><br><br>
                        Use small datasets to predict patterns — for example, energy demand or pollution spread.  
                        Experiment with open libraries like TensorFlow or PyTorch.  
                        Collaborate in online hackathons for green AI innovation.  
                        You are now learning how data and ethics intersect.
                        """,
                        "90": """
                        <b>Final 90 Days — Showcase AI for Impact</b><br><br>
                        Document your work in a clear case study.  
                        Publish a short article or visual demo highlighting environmental outcomes your model supports.  
                        Focus on accessibility — explain complex ideas simply.  
                        You now embody the role of a sustainability innovator.
                        """
                    },

                    "Circular Design": {
                        "30": """
                        <b>First 30 Days — Rethink Waste</b><br><br>
                        Learn lifecycle thinking — how products move from creation to disposal.  
                        Identify pain points in current design processes and where waste can become value.  
                        Study global examples like Loop or Terracycle to understand circular innovation.
                        """,
                        "60": """
                        <b>Next 60 Days — Create Low-Waste Solutions</b><br><br>
                        Sketch redesigns for common items — a refillable bottle, biodegradable packaging, or reuse systems.  
                        Prototype small ideas using recycled materials or design software.  
                        Engage peers for quick feedback.
                        """,
                        "90": """
                        <b>Final 90 Days — Share Your Circular Vision</b><br><br>
                        Prepare a visual presentation of your project.  
                        Communicate the social and environmental impact clearly.  
                        Apply to student competitions or local circular hackathons.  
                        You now act as a designer for regeneration, not consumption.
                        """
                    },

                    "Smart Mobility": {
                        "30": """
                        <b>First 30 Days — Learn Mobility Ecosystems</b><br><br>
                        Research how cities integrate public transport, cycling, and electric mobility.  
                        Understand how sustainable transport reduces emissions and improves equality.  
                        Watch case videos from Singapore and Copenhagen.
                        """,
                        "60": """
                        <b>Next 60 Days — Map and Model Change</b><br><br>
                        Use GIS or simulation tools to visualize mobility data.  
                        Conduct small surveys about commuting behavior.  
                        Start thinking about incentives — how to shift user habits from cars to green modes.
                        """,
                        "90": """
                        <b>Final 90 Days — Design Mobility Solutions</b><br><br>
                        Develop a mini proposal — such as bike-sharing networks or smart transit.  
                        Present the idea to classmates or local NGOs.  
                        You are now shaping sustainable urban mobility narratives.
                        """
                    },

                    "Project Management": {
                        "30": """
                        <b>First 30 Days — Learn Green Project Basics</b><br><br>
                        Study Agile and design thinking principles.  
                        Begin managing small environmental awareness activities or campus projects.  
                        Reflect on how leadership works in sustainability teams.
                        """,
                        "60": """
                        <b>Next 60 Days — Coordinate Impact Work</b><br><br>
                        Plan and execute a sustainability event.  
                        Track resources, communicate timelines, and evaluate risks.  
                        Build communication rhythm with your team — this is real leadership practice.
                        """,
                        "90": """
                        <b>Final 90 Days — Lead and Reflect</b><br><br>
                        Compile your project outcomes and lessons learned.  
                        Create a one-page summary highlighting measurable impacts.  
                        Apply your learning to apply for sustainability program coordinator roles.
                        """
                    },

                    "Behavioral Change Design": {
                        "30": """
                        <b>First 30 Days — Study Human Habits</b><br><br>
                        Learn behavioral frameworks like Nudge Theory and Choice Architecture.  
                        Understand why people resist or adopt sustainable actions.  
                        Begin tracking your own behaviors as an experiment.
                        """,
                        "60": """
                        <b>Next 60 Days — Test Real Interventions</b><br><br>
                        Design small behavior-change challenges, e.g., “Plastic-Free Week.”  
                        Measure participation and collect feedback.  
                        You’re now testing social influence in sustainability.
                        """,
                        "90": """
                        <b>Final 90 Days — Evaluate and Communicate</b><br><br>
                        Document your process and results.  
                        Reflect on emotional, social, and cognitive barriers.  
                        Share findings in a short article or infographic.  
                        You are now able to link behavioral science with environmental design.
                        """
                    },

                    "Sustainable Finance": {
                        "30": """
                        <b>First 30 Days — Learn ESG Investment Basics</b><br><br>
                        Understand how finance can enable green transitions.  
                        Study ESG standards, SDG investment frameworks, and key KPIs.  
                        Follow green bond news to see capital flow into impact sectors.
                        """,
                        "60": """
                        <b>Next 60 Days — Analyze Real Financial Impact</b><br><br>
                        Review sustainability reports and identify investment priorities.  
                        Learn tools like SASB or IRIS+ to assess social and environmental returns.  
                        Practice interpreting case studies on renewable or circular startups.
                        """,
                        "90": """
                        <b>Final 90 Days — Build a Green Investment Proposal</b><br><br>
                        Simulate an investment case with projected ROI and SDG impact.  
                        Present it as a “pitch deck” to mentors or classmates.  
                        You now bridge the gap between finance and sustainability action.
                        """
                    },

                    "Environmental Policy": {
                        "30": """
                        <b>First 30 Days — Understand Global Frameworks</b><br><br>
                        Study the Paris Agreement, SDGs, and ASEAN sustainability commitments.  
                        Identify how policies influence green industry transitions.  
                        Learn how local regulation translates into corporate change.
                        """,
                        "60": """
                        <b>Next 60 Days — Evaluate Local Implementation</b><br><br>
                        Pick one policy (like renewable incentives) and analyze how it works in practice.  
                        Interview community members or businesses.  
                        This develops critical thinking on system change.
                        """,
                        "90": """
                        <b>Final 90 Days — Design a Policy Proposal</b><br><br>
                        Write a short recommendation paper on improving existing policies.  
                        Highlight trade-offs and fairness.  
                        Share with university networks or NGOs — you are now a policy innovator.
                        """
                    }
                }

                # -----------------------------
                # 展示生成结果
                # -----------------------------
                for skill in selected_skills:
                    st.markdown(f"<h3 style='color:#2E8B57; margin-top:25px;'>💡 {skill} Growth Path</h3>", unsafe_allow_html=True)
                    for phase in ["30", "60", "90"]:
                        st.markdown(f"""
                        <div style="
                            background-color:#f8fcf9;
                            border-radius:15px;
                            padding:20px;
                            margin-top:15px;
                            box-shadow:0 3px 8px rgba(46,139,87,0.15);
                            border-left:5px solid #2E8B57;
                        ">
                            {plans[skill][phase]}
                        </div>
                        """, unsafe_allow_html=True)

                st.success("🌱 Each pathway offers a structured route from awareness to action — choose consistency over intensity for sustainable growth.")

        # -----------------------------
        # 📘 AI Suggested Next Step 模块（独立版，缩进已统一）
        # -----------------------------
        st.markdown("---")
        st.markdown("<h3 style='color:#1b4332;'>📘 AI Suggested Next Step</h3>", unsafe_allow_html=True)

        # 单技能建议
        next_step_single = {
            "Data Analysis": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            Developing a career in <b>Data Analysis for Sustainability</b> requires both technical literacy and ethical interpretation.  
            Over the coming months, you should apply your quantitative skills to social and environmental datasets, moving beyond descriptive analytics into predictive modeling.  
            Focus on understanding causal relationships, uncertainty, and data ethics — these competencies differentiate analytical technicians from evidence-based decision-makers.  
            Participating in open-data sustainability projects and publishing applied research will help you translate numbers into real-world influence.  
            </div>
            """,

            "Carbon Accounting": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            Advancing in <b>Carbon Accounting</b> involves moving from numerical reporting toward strategic sustainability insight.  
            You should focus on understanding the interdependence between corporate behavior, regulation, and transparency mechanisms such as ESG reporting.  
            In-depth study of carbon offset frameworks and lifecycle emissions can position you as a credible professional capable of integrating environmental metrics into business logic.  
            This skill maturity supports future leadership in sustainable finance and climate disclosure strategy.  
            </div>
            """,

            "Renewable Energy": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            With growing renewable knowledge, your next step is to integrate <b>technical design</b> and <b>systemic policy</b> perspectives.  
            Deepen understanding of energy economics and community participation models.  
            Engage in interdisciplinary research exploring the feasibility of localized solar or wind microgrids.  
            This synthesis between engineering and governance equips you to contribute to equitable and scalable clean energy transitions across Southeast Asia.  
            </div>
            """,

            "AI for Sustainability": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            Your focus should now shift toward designing explainable and ethically responsible AI systems for sustainability applications.  
            Consider integrating environmental data into supervised learning pipelines, emphasizing interpretability and bias mitigation.  
            Publishing results in open-source repositories can amplify your professional credibility.  
            At this level, your goal is to demonstrate how intelligent systems can improve environmental monitoring and support policy innovation responsibly.  
            </div>
            """,

            "Circular Design": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            As a <b>Circular Designer</b>, your next goal is to operationalize theory through systemic experimentation.  
            Explore collaborations with manufacturers, focusing on materials innovation, reverse logistics, and life-cycle optimization.  
            Research on behavioral economics and design psychology will further enhance your ability to influence sustainable consumption patterns.  
            Combining creativity with measurable sustainability impact defines leadership in this emerging discipline.  
            </div>
            """,

            "Smart Mobility": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            To advance in <b>Smart Mobility</b>, move beyond infrastructure to behavioral and data perspectives.  
            Use mobility analytics to evaluate commuter patterns and policy effectiveness.  
            Focus on integrating clean transport technology with social inclusion.  
            Your long-term professional maturity lies in designing urban mobility ecosystems that merge equity, safety, and carbon efficiency.  
            </div>
            """,

            "Project Management": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            As a sustainability-oriented project manager, your emphasis should now be on systems leadership and evidence-based evaluation.  
            Study agile methodologies adapted for climate innovation and impact assessment.  
            Learning to balance stakeholder communication, financial accountability, and ecological value will enable you to manage high-complexity sustainability programs.  
            Documenting results transparently strengthens institutional learning and policy advocacy.  
            </div>
            """,

            "Behavioral Change Design": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            The next academic leap involves mastering evaluation design for behavioral interventions.  
            Learn advanced social psychology, data collection, and ethics of influence.  
            Combining qualitative research with digital communication strategies can expand your reach.  
            At this stage, your focus should be on measurable impact — shaping long-term habits rather than short-term change.  
            </div>
            """,

            "Sustainable Finance": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            Strengthen your analytical and ethical foundation by connecting finance with climate science.  
            Engage in carbon pricing simulation, impact valuation, and ESG materiality assessment.  
            Understanding the interplay between risk management and social return on investment will prepare you for leadership in sustainable financial innovation.  
            Join academic communities focused on impact measurement to expand your research lens.  
            </div>
            """,

            "Environmental Policy": """
            <div style="background:linear-gradient(120deg,#e8f7ef,#dff9e3);padding:25px;border-radius:18px;box-shadow:0 5px 15px rgba(46,139,87,0.25);">
            <b>AI Academic Recommendation:</b><br><br>
            Your progression in <b>Environmental Policy</b> should now target analytical depth and diplomatic communication.  
            Focus on policy impact evaluation and negotiation mechanisms within global governance.  
            Develop cross-sector understanding of law, economics, and behavioral sciences.  
            Publish policy briefs or opinion essays to strengthen your voice as a researcher-practitioner influencing equitable transitions.  
            </div>
            """
        }

        # 如果只选择一个技能
        if len(selected_skills) == 1:
            st.markdown(next_step_single[selected_skills[0]], unsafe_allow_html=True)

        # 如果选择两个技能，生成融合总结
        elif len(selected_skills) == 2:
            s1, s2 = selected_skills
            combined_text = f"""
            <div style="background:linear-gradient(135deg,#d8f3dc,#e6f4ea);padding:30px;border-radius:20px;box-shadow:0 6px 14px rgba(46,139,87,0.25);">
            <b>AI Integrated Academic Recommendation:</b><br><br>
            By integrating <b>{s1}</b> and <b>{s2}</b>, you are building a hybrid expertise that reflects the interdisciplinary nature of future sustainability professions.  
            You should now design a project that merges the quantitative and qualitative dimensions of green transformation — for instance, using {s1.lower()} to inform or enhance {s2.lower()} outcomes.  
            Such integration nurtures strategic foresight, systems reasoning, and creative leadership.  
            Your 90-day goal should be to prototype a real-world application linking both domains and document how this synthesis can reduce systemic barriers to sustainable innovation.  
            This meta-level capacity for connecting tools, people, and impact is precisely what defines next-generation sustainability leadership.  
            </div>
            """
            st.markdown(combined_text, unsafe_allow_html=True)

        st.success("🌿 Your AI-guided academic recommendation translates learning into professional strategy.")




                        # -----------------------------
    # Section 4: Smart Summary (Final Clean Version)
    # -----------------------------
    elif section == "Smart Summary":
        import pandas as pd
        from fpdf import FPDF
        from io import BytesIO
        import base64
        from datetime import datetime

        st.markdown("<h2 style='color:#2E8B57;'>🌍 Smart Sustainability Career Insight Hub</h2>", unsafe_allow_html=True)
        st.caption("A reliable, elegant, and fully functional analytics dashboard for green careers.")

        # ========= Filters =========
        st.markdown("### 🎯 Customize Your View")
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_city = st.selectbox("🏙️ City", ["All"] + sorted(jobs_df["City"].fillna("").unique().tolist()))
        with col2:
            selected_skill = st.selectbox("🧠 Skill", ["All"] + sorted(set(", ".join(jobs_df["KeySkills"].fillna("")).split(", "))))
        with col3:
            selected_category = st.selectbox("🌱 Category", ["All"] + sorted(jobs_df["Category"].fillna("").unique().tolist()))

        filtered_df = jobs_df.fillna("").copy()
        if selected_city != "All":
            filtered_df = filtered_df[filtered_df["City"].str.contains(selected_city, case=False)]
        if selected_skill != "All":
            filtered_df = filtered_df[filtered_df["KeySkills"].str.contains(selected_skill, case=False)]
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["Category"].str.contains(selected_category, case=False)]

        if filtered_df.empty:
            st.warning("⚠️ No data found for this filter. Try another combination.")
            st.stop()

        # ========= Overview Cards =========
        total_jobs = len(filtered_df)
        avg_score = round(filtered_df["MatchScore"].mean(), 1)
        active_cities = filtered_df["City"].nunique()

        st.markdown(f"""
        <div style='display:flex; justify-content:space-around; margin:15px 0;'>
            <div style='background:#e8f5e9; padding:18px 25px; border-radius:10px; width:30%; text-align:center;'>
                <h3 style='color:#2E8B57;'>📈 {total_jobs}</h3>
                <p>Total Opportunities</p>
            </div>
            <div style='background:#e0f2f1; padding:18px 25px; border-radius:10px; width:30%; text-align:center;'>
                <h3 style='color:#00796b;'>{avg_score}</h3>
                <p>Average Match Score</p>
            </div>
            <div style='background:#f1f8e9; padding:18px 25px; border-radius:10px; width:30%; text-align:center;'>
                <h3 style='color:#33691e;'>{active_cities}</h3>
                <p>Active Cities</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ========= Charts =========
        try:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🌆 Top Cities by Job Count")
                city_counts = filtered_df["City"].value_counts().head(6)
                st.bar_chart(city_counts)

            with col2:
                st.markdown("#### 💼 Leading Job Categories")
                cat_counts = filtered_df["Category"].value_counts().head(6)
                st.bar_chart(cat_counts)
        except Exception as e:
            st.error(f"Chart error: {e}")

        st.markdown("---")

        try:
            col3, col4 = st.columns(2)
            with col3:
                st.markdown("#### 🔑 Most In-Demand Skills")
                all_skills = []
                for s in filtered_df["KeySkills"]:
                    all_skills.extend([x.strip() for x in s.split(",")])
                skill_counts = pd.Series(all_skills).value_counts().head(8)
                st.bar_chart(skill_counts)

            with col4:
                st.markdown("#### 📊 Average Match Score by Category")
                avg_scores = filtered_df.groupby("Category")["MatchScore"].mean().sort_values(ascending=False)
                st.line_chart(avg_scores)
        except Exception as e:
            st.error(f"Data error: {e}")

        # ========= AI Summary =========
        st.markdown("---")
        st.markdown("### 🤖 AI Insight Summary")

        try:
            top_city = city_counts.index[0]
            top_cat = cat_counts.index[0]
            top_skill = skill_counts.index[0]
        except:
            top_city, top_cat, top_skill = "N/A", "N/A", "N/A"

        ai_text = f"""
        🌱 Regional Outlook:  
        The sustainability job market in {top_city} is thriving, especially in {top_cat}.  
        Professionals skilled in {top_skill} are driving transformation through measurable environmental impact.  

        💡 Market Dynamics:  
        Organizations are shifting from symbolic ESG initiatives toward data-driven sustainability integration.  
        The rise of hybrid roles such as carbon analysts and eco-data strategists reflects a new employment frontier.  

        🎯 Strategic Takeaway:  
        Interdisciplinary talent that bridges technology and sustainability will lead Asia-Pacific’s transition to a low-carbon economy.
        """
        st.markdown(f"<div style='background:#f9fff9; border-left:5px solid #2E8B57; padding:18px; border-radius:10px; white-space:pre-wrap;'>{ai_text}</div>", unsafe_allow_html=True)




        # ========= SMART ACTION SUGGESTIONS (Final Refined UI with Split Titles) =========
        st.markdown("---")
        st.markdown("<h3 style='color:#1b4332;'>🧭 Smart Action Suggestions</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:gray; font-size:14px;'>AI-generated recommendations to help you act on insights and advance your sustainability career.</p>", unsafe_allow_html=True)

        # Dynamic subtitle
        st.markdown(
            f"<div style='background:#f0fdf4; border-radius:8px; padding:8px 15px; margin-bottom:15px; color:#1b4332; font-size:14px;'>"
            f"Based on your filters: <b>{selected_city}</b> | <b>{selected_skill}</b> | <b>{selected_category}</b></div>",
            unsafe_allow_html=True
        )

        # --- Text content ---
        learning_title = "🎓 Learning Path"
        learning_body = (
            f"Deepen your expertise in {top_skill} through online certifications or micro-courses on Coursera or edX. "
            f"Apply your knowledge within {top_cat.lower()} contexts to develop stronger analytical and implementation skills."
        )

        networking_title = "🤝 Networking"
        networking_body = (
            f"Join sustainability networks and professional groups in {top_city}, such as ClimateTech meetups or ESG associations. "
            f"Engage with peers and mentors to exchange insights and expand your influence in the green economy."
        )

        career_title = "🚀 Career Move"
        career_body = (
            f"Explore emerging roles like Sustainability Data Strategist or Green Innovation Analyst. "
            f"These align with current trends in {top_cat.lower()} and demand for {top_skill.lower()} expertise in sustainable transformation."
        )

        # --- Card layout ---
        col1, col2, col3 = st.columns(3)
        card_style = (
            "background:#f7fff7; border-left:5px solid #2E8B57; border-radius:10px; "
            "padding:18px 15px; box-shadow:0 1px 5px rgba(0,0,0,0.05); height:180px;"
        )
        title_style = "font-size:17px; font-weight:600; color:#1b4332; margin-bottom:6px;"
        body_style = "font-size:15px; color:#2d6a4f; line-height:1.5;"

        with col1:
            st.markdown(
                f"<div style='{card_style}'>"
                f"<div style='{title_style}'>{learning_title}</div>"
                f"<div style='{body_style}'>{learning_body}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div style='{card_style}'>"
                f"<div style='{title_style}'>{networking_title}</div>"
                f"<div style='{body_style}'>{networking_body}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div style='{card_style}'>"
                f"<div style='{title_style}'>{career_title}</div>"
                f"<div style='{body_style}'>{career_body}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        # --- Footer Tip ---
        st.markdown(
            "<p style='color:#495057; font-size:13px; margin-top:10px;'>💡 Tip: "
            "You can integrate these actions into your <b>30/60/90 Career Plan</b> section for measurable learning, networking, and career impact goals.</p>",
            unsafe_allow_html=True
        )


    # -----------------------------
    # Section 5: Green Coach Chat
    # -----------------------------
    elif section == "Green Coach Chat":
        st.markdown("<h2 style='color:#2E8B57;'>🤖 Green Coach Chat</h2>", unsafe_allow_html=True)
        st.caption("Your personal AI sustainability mentor — choose your coach, ask questions, and receive tailored, thoughtful insights to guide your green career journey.")

        # -----------------------------
        # 🌿 Role Selection (Card UI)
        # -----------------------------
        st.markdown("### 🧭 Choose Your Coach")
        roles = {
            "Career Planner": "📘 Helps you align your personal goals with sustainable career pathways.",
            "Skill Trainer": "🧠 Guides you to identify, learn, and enhance future-ready green skills.",
            "Motivation Buddy": "🔥 Keeps you inspired, confident, and resilient on your sustainability journey."
        }

        cols = st.columns(3)
        selected_role = st.session_state.get("selected_role", None)

        for i, (role, desc) in enumerate(roles.items()):
            with cols[i]:
                card_color = '#d8f3dc' if st.session_state.get("selected_role") == role else '#f8f9fa'
                border_color = '#2d6a4f' if st.session_state.get("selected_role") == role else '#d8f3dc'
                st.markdown(
                    f"""
                    <div style="
                        background-color:{card_color};
                        border:2px solid {border_color};
                        border-radius:15px;
                        padding:15px;
                        box-shadow:0 3px 8px rgba(0,0,0,0.08);
                        text-align:center;
                        transition:0.3s;">
                        <h4 style='margin-bottom:6px;'>{role}</h4>
                        <p style='font-size:13px;color:#444;'>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                if st.button(role):
                    st.session_state.selected_role = role
                    st.session_state.chat_history = []  # 清空历史

        selected_role = st.session_state.get("selected_role", None)

        # -----------------------------
        # 💬 Display Questions
        # -----------------------------
        if selected_role:
            st.markdown(f"#### 🌱 You are chatting with: **{selected_role}**")

            questions = {
                "Career Planner": [
                    "How can I identify sustainable career opportunities that align with my strengths?",
                    "What industries are expected to grow fastest in green employment?",
                    "How can I transition my current role into the sustainability field?",
                    "What certifications or qualifications will enhance my sustainable career prospects?",
                    "How can I showcase my green values in job interviews?",
                    "How do I plan a 5-year growth path in the green economy?",
                    "What are common challenges when pursuing sustainability roles?",
                    "How can I balance income goals with impact-driven work?"
                ],
                "Skill Trainer": [
                    "What technical skills are most valuable in sustainability careers?",
                    "How can I learn data analysis for environmental projects?",
                    "Which online platforms are best for green upskilling?",
                    "How do I combine AI and sustainability effectively?",
                    "What soft skills should I develop for sustainable leadership?",
                    "How do I evaluate my current skill gaps?",
                    "What are emerging skill trends in green industries?",
                    "How can I apply what I learn in real-world sustainability projects?"
                ],
                "Motivation Buddy": [
                    "How do I stay motivated while job searching in sustainability?",
                    "How can I overcome fear of failure when changing careers?",
                    "What can I do when I feel my sustainability efforts don’t make an impact?",
                    "How do I stay confident when others don’t value green careers?",
                    "How can I find like-minded people who share my mission?",
                    "How do I manage stress from trying to make a difference?",
                    "What is the best way to maintain long-term passion for sustainability?",
                    "How can I celebrate small wins on this journey?"
                ]
            }

            # 用户选择问题
            user_question = st.selectbox("💭 Choose a question:", questions[selected_role])

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # 模拟提问
            if st.button("Ask Green Coach", use_container_width=True):
                st.session_state.chat_history.append(("user", user_question))
                # -----------------------------
                # 🤖 Green Coach Responses
                # -----------------------------
                responses = {
                    "Career Planner": {
                        "How can I identify sustainable career opportunities that align with my strengths?":
                            "Insight: Begin by mapping your core values, preferred work style, and long-term aspirations. Sustainable careers span across disciplines—finance, data, design, policy—so alignment often depends on how your personal motivations intersect with global sustainability goals. Next Step: Use self-assessment tools such as the SDG Compass or UN Career Pathfinder to identify where your skills meet environmental or social impact needs. Resource Tip: Explore real case examples in the World Economic Forum’s 'Future of Jobs' report to visualize skill-to-impact connections.",
                        "What industries are expected to grow fastest in green employment?":
                            "Insight: The renewable energy sector continues to dominate, with solar and wind expansion leading job creation across Asia-Pacific. Other high-growth domains include sustainable urban planning, electric mobility, ESG analytics, and circular economy design. Next Step: Focus your research on industries that combine both technological innovation and public policy incentives. Resource Tip: Review IRENA’s Global Energy Transformation Outlook for regional employment projections and transition readiness.",
                        "How can I transition my current role into the sustainability field?":
                            "Insight: Transitioning into sustainability does not require abandoning your current profession. Instead, integrate sustainability principles into your field—marketing can pivot to ethical branding, finance to impact investing, or engineering to green design. Next Step: Start with sustainability certifications and company CSR involvement to build credibility internally. Resource Tip: Explore the 'One Planet Academy' and LinkedIn’s Sustainable Strategy micro-courses to craft a transition narrative aligned with measurable impact.",
                        "What certifications or qualifications will enhance my sustainable career prospects?":
                            "Insight: Credentials such as LEED, GRI, CFA ESG, or ISO 14001 auditor qualifications are internationally recognized. However, practical experience—project leadership, volunteering, or innovation challenges—often outweighs theoretical certificates. Next Step: Choose a certificate that complements your academic background and career stage rather than chasing popularity. Resource Tip: Visit Coursera’s Sustainability Leadership catalogue or the UN CC:Learn hub for recognized global certifications.",
                        "How can I showcase my green values in job interviews?":
                            "Insight: Employers value authenticity more than slogans. Frame your sustainability experience through evidence—projects, measurable outcomes, and lessons learned. Use the STAR method (Situation, Task, Action, Result) to illustrate your environmental mindset in concrete actions. Next Step: Practice articulating how your personal mission aligns with organizational SDG goals. Resource Tip: Read 'Communicating Impact' by Harvard Business Review to refine your storytelling and professional branding.",
                        "How do I plan a 5-year growth path in the green economy?":
                            "Insight: A successful 5-year plan balances adaptability with intention. The sustainability field evolves quickly; new technologies emerge annually. Plan around capability milestones rather than job titles—learning a new analytical tool, leading a project, or contributing to a publication. Next Step: Map your progression through yearly skill goals. Resource Tip: Use tools like Trello or Notion to visualize long-term competence building linked to global climate objectives.",
                        "What are common challenges when pursuing sustainability roles?":
                            "Insight: Many professionals face frustration over limited entry-level opportunities or unclear career ladders. Others struggle with organizations that engage in greenwashing rather than real transformation. Next Step: Evaluate employers critically using transparency reports and third-party ESG ratings. Resource Tip: Consult the BCorp directory and the Ethical Consumer Index to target authentic sustainability-driven employers.",
                        "How can I balance income goals with impact-driven work?":
                            "Insight: Financial stability and meaningful impact are not mutually exclusive. The key lies in finding hybrid positions—consultancy, data analytics, or project management—where environmental outcomes align with market value. Next Step: Develop negotiation skills and communicate the business value of sustainability initiatives to justify compensation. Resource Tip: Read the 'Sustainability Salary Guide' by Acre for insights on pay ranges and advancement routes."
                    },
                    "Skill Trainer": {
                        "What technical skills are most valuable in sustainability careers?":
                            "Insight: The intersection of technology and sustainability is where future impact will occur. Data analytics, life-cycle assessment, and systems thinking are indispensable. Coding proficiency, especially in Python or R, enhances employability. Next Step: Build proficiency through applied projects rather than theory. Join hackathons focused on energy efficiency or smart city modeling. Resource Tip: Explore the MIT OpenCourseWare series on Climate Informatics and Data Analytics for Climate Science.",
                        "How can I learn data analysis for environmental projects?":
                            "Insight: Start with foundational courses in data analytics, focusing on environmental datasets. Learn visualization tools like Power BI or Tableau to translate data into action. Next Step: Select one environmental topic—waste, air quality, or energy—and analyze open datasets. Document findings through a mini-report or dashboard. Resource Tip: Use the World Bank Data Catalogue and Kaggle’s climate datasets for practice material.",
                        "Which online platforms are best for green upskilling?":
                            "Insight: Coursera, FutureLearn, and edX now offer structured green skills pathways endorsed by top universities. For more technical expertise, consider ESRI’s GIS or Google’s Sustainability Data programs. Next Step: Dedicate one learning sprint per month. Record progress and share reflections on LinkedIn for credibility. Resource Tip: Access UNITAR’s Green Learning Portal for public sector sustainability leadership modules.",
                        "How do I combine AI and sustainability effectively?":
                            "Insight: AI enhances sustainability through predictive modeling and optimization. Use machine learning to simulate carbon emissions or track biodiversity changes. However, ethical constraints—energy consumption and bias—must guide usage. Next Step: Experiment with small-scale ML models using public APIs for environmental forecasting. Resource Tip: Engage with 'AI for Earth' by Microsoft and DeepMind’s Climate Action research papers.",
                        "What soft skills should I develop for sustainable leadership?":
                            "Insight: Communication, empathy, and strategic foresight matter as much as technical knowledge. The capacity to translate science into policy and inspire interdisciplinary collaboration defines sustainable leadership. Next Step: Practice systems thinking workshops and cross-sector dialogues. Resource Tip: Read the Cambridge Institute’s 'Leading for Change' series and engage in reflective journaling.",
                        "How do I evaluate my current skill gaps?":
                            "Insight: Use skill mapping frameworks like LinkedIn Learning’s Sustainability Map or ILO’s Green Competence Framework. Honest self-assessment fosters targeted growth. Next Step: Identify one hard skill and one soft skill to strengthen quarterly. Resource Tip: Review the 'Green Skills Report 2024' for benchmark comparisons.",
                        "What are emerging skill trends in green industries?":
                            "Insight: Green finance, circular design, and renewable integration dominate job trends. Companies seek professionals who bridge technology and sustainability policy. Next Step: Subscribe to newsletters like 'GreenBiz Skills Weekly'. Resource Tip: Read the WEF’s 'Jobs of Tomorrow' report to anticipate demand.",
                        "How can I apply what I learn in real-world sustainability projects?":
                            "Insight: Application solidifies knowledge. Partner with NGOs or student-led innovation labs. Field practice reveals context beyond theory. Next Step: Choose one ongoing community project to contribute to each semester. Resource Tip: Explore UN Volunteers or OpenIDEO project challenges for experiential learning."
                    },
                    "Motivation Buddy": {
                        "How do I stay motivated while job searching in sustainability?":
                            "Insight: Green careers often progress slower because they demand passion over prestige. Motivation strengthens when you redefine success as alignment with purpose. Next Step: Maintain a progress journal and join professional communities like Net Impact for peer support. Resource Tip: Listen to the 'Sustainability Leaders' podcast to hear real-life transition stories.",
                        "How can I overcome fear of failure when changing careers?":
                            "Insight: Failure is feedback, not defeat. Every professional pivot includes uncertainty. Sustainability fields reward adaptability and persistence. Next Step: Reflect on learning milestones from setbacks and share insights publicly. Resource Tip: Read 'Grit' by Angela Duckworth for long-term resilience mindset building.",
                        "What can I do when I feel my sustainability efforts don’t make an impact?":
                            "Insight: Individual contributions are building blocks of systemic change. Shift focus from control to contribution. Next Step: Collaborate with local organizations to visualize collective outcomes. Resource Tip: Join Climate Action Tracker to measure global policy progress and link your work contextually.",
                        "How do I stay confident when others don’t value green careers?":
                            "Insight: Confidence grows from evidence-based conviction. Green jobs now outpace fossil sectors in growth and profitability. Next Step: Equip yourself with data showcasing sustainability ROI to advocate effectively. Resource Tip: Access the ILO Green Jobs Programme for proof-driven narratives.",
                        "How can I find like-minded people who share my mission?":
                            "Insight: Belonging amplifies commitment. Connect through social innovation networks, hackathons, and sustainability hubs. Next Step: Join Slack communities like 'Work on Climate'. Resource Tip: Explore the Impact Hub Global directory to find changemakers.",
                        "How do I manage stress from trying to make a difference?":
                            "Insight: Sustainability work can feel emotionally heavy. Practice balance through structured rest and reflection. Next Step: Schedule non-digital downtime and eco-anxiety workshops. Resource Tip: Follow Mindful Earth’s mental wellbeing toolkit.",
                        "What is the best way to maintain long-term passion for sustainability?":
                            "Insight: Passion matures when tied to learning. Diversify exposure—alternate technical learning with community engagement. Next Step: Set annual reflection goals tied to global events (Earth Day, COP). Resource Tip: Explore the Pachamama Alliance for purpose renewal.",
                        "How can I celebrate small wins on this journey?":
                            "Insight: Gratitude and recognition fuel sustainable motivation. Share milestones publicly to normalize slow progress. Next Step: Keep a monthly reflection tracker. Resource Tip: Try Habitica to gamify your achievements and sustain engagement."
                    }
                }

                # -----------------------------
                # 💬 Display Chat History (Bubble UI)
                # -----------------------------
                st.markdown("---")
                for sender, msg in st.session_state.chat_history:
                    if sender == "user":
                        st.markdown(
                            f"""
                            <div style="text-align:right; background-color:#d8f3dc; 
                            padding:10px; border-radius:15px; margin:8px 0 8px 40px;">
                            👤 <b>You:</b> {msg}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f"""
                            <div style="text-align:left; background-color:#f1f1f1;
                            padding:12px; border-radius:15px; margin:8px 40px 8px 0;">
                            🤖 <b>Green Coach:</b><br>{msg.replace('Insight:', '<b>Insight:</b>').replace('Next Step:', '<br><b>Next Step:</b>').replace('Resource Tip:', '<br><b>Resource Tip:</b>')}
                            </div>
                            """, unsafe_allow_html=True)

                # -----------------------------
                # 🧠 Generate AI Response
                # -----------------------------
                if st.session_state.chat_history and st.session_state.chat_history[-1][0] == "user":
                    q = st.session_state.chat_history[-1][1]
                    answer = responses[selected_role].get(q, "I’m processing this request, please try again.")
                    st.session_state.chat_history.append(("coach", answer))
                    st.experimental_rerun()













            # -----------------------------
    # Section 6: Dashboard (Upgraded Smart Version)
    # -----------------------------
    elif section == "Dashboard":
        import altair as alt
        import numpy as np

        st.markdown("""
        <div style='background:linear-gradient(to bottom, #edf8ef, #ffffff); padding:20px; border-radius:15px;'>
            <h2 style='color:#2E8B57; text-align:center;'>📊 My Green Career Dashboard</h2>
            <p style='text-align:center; color:#4b6043;'>AI-driven insights into your learning journey, growth potential, and sustainability readiness.</p>
        </div>
        """, unsafe_allow_html=True)

        # -----------------------------
        # 🌿 Overview Summary
        # -----------------------------
        st.markdown("### 🌿 Overview Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric("Skill Alignment", "82%", "↑ 5% vs last month")
        col2.metric("Career Readiness", "Intermediate", "🚀 Progressing")
        col3.metric("Sustainability Impact", "High", "+12% community engagement")

        st.progress(0.82)
        st.caption("Your profile shows strong momentum toward green career alignment, combining data-driven skills and sustainability values.")

        st.markdown("---")

        # -----------------------------
        # 🧠 Skill Progress vs Market Demand
        # -----------------------------
        st.markdown("### 🧠 Skill Progress vs Market Demand")

        skills = ["Data Analysis", "Carbon Accounting", "ESG Reporting", "AI for Sustainability", "Stakeholder Engagement"]
        user_level = [78, 65, 58, 71, 84]
        market_avg = [70, 75, 63, 68, 80]

        df_skill = pd.DataFrame({
            "Skill": skills,
            "User": user_level,
            "Market": market_avg
        })

        chart = alt.Chart(df_skill.melt('Skill')).mark_bar().encode(
            x=alt.X('Skill:N', title=None),
            y=alt.Y('value:Q', title='Proficiency (%)'),
            color=alt.Color('variable:N', scale=alt.Scale(range=['#52b788', '#95d5b2']), legend=alt.Legend(title="Comparison")),
            tooltip=['Skill', 'variable', 'value']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

        # -----------------------------
        # 🧠 1. Dynamic AI Insight Summary
        # -----------------------------
        avg_skill = np.mean(user_level)
        weakest = skills[np.argmin(user_level)]
        strongest = skills[np.argmax(user_level)]
        improvement_gap = abs(user_level[np.argmin(user_level)] - market_avg[np.argmin(user_level)])

        ai_summary = f"""
        **AI Insight:** Your average skill alignment is **{avg_skill:.0f}%**, showing steady progress across domains.
        Your strongest area is **{strongest}**, exceeding the market average by {user_level[np.argmax(user_level)] - market_avg[np.argmax(user_level)]}%.
        However, **{weakest}** lags behind market standards by {improvement_gap}%, which presents an immediate upskilling opportunity.

        **Next Step:** Allocate focused learning time toward {weakest}, especially through project-based practice and mentorship.

        **Resource Tip:** Explore the *UN SDG Learning Hub* or *LinkedIn Learning ESG Series* for short, applied modules that build both technical and strategic green expertise.
        """
        st.info(ai_summary)

        st.markdown("---")

        # -----------------------------
        # 🎯 Career Path Progress + Growth Forecast
        # -----------------------------
        st.markdown("### 🎯 Career Path Progress & Growth Forecast")

        timeline = pd.DataFrame({
            'Stage': ['30 Days', '60 Days', '90 Days'],
            'Completion': [85, 60, 35]
        })

        chart_timeline = alt.Chart(timeline).mark_bar(color='#1b4332').encode(
            x='Stage',
            y='Completion',
            tooltip=['Stage', 'Completion']
        ).properties(height=250)
        st.altair_chart(chart_timeline, use_container_width=True)

        # Growth forecast simulation
        growth = np.polyfit([0, 30, 60, 90], [80, 82, 85, 89], 1)
        predicted = [growth[0]*x + growth[1] for x in [30, 60, 90]]

        forecast_df = pd.DataFrame({
            "Timeline (Days)": ["30", "60", "90"],
            "Predicted Match Score": predicted
        })

        chart_forecast = alt.Chart(forecast_df).mark_line(point=True, color="#2E8B57").encode(
            x="Timeline (Days)",
            y="Predicted Match Score",
            tooltip=["Timeline (Days)", "Predicted Match Score"]
        ).properties(height=250)

        st.altair_chart(chart_forecast, use_container_width=True)
        st.caption("📈 Based on your current learning rate, you’re projected to reach 90% green career readiness within the next three months.")

        st.markdown("---")

        # -----------------------------
        # 🧭 3. Smart Action Recommendations
        # -----------------------------
        st.markdown("### 🧭 Smart AI Recommendations")

        st.success(f"""
        **Priority Focus:** {weakest}  
        **Why it matters:** This skill bridges technical capacity with sustainability impact — a growing requirement in future leadership roles.  

        **Suggested Actions:**  
        - Join a short-term applied workshop on {weakest}  
        - Apply your learning to a micro-project (e.g., local carbon offset analysis or energy audit simulation)  
        - Network with professionals through sustainability LinkedIn groups or the Green Jobs Asia Forum  

        **Resource Tip:** Explore *Google Sustainability Learning*, *UN Climate Academy*, or *Coursera’s Green Tech Track* to gain structured learning paths.  
        """)

        st.info("""
        💬 *Insight:* Balancing technical depth with social awareness is key to thriving in the next decade of green transformation.  
        Sustainability leaders are those who integrate systems thinking with innovation and empathy.
        """)

        st.markdown("---")

    # -----------------------------
    # 🌍 Section: Green Economy Reality
    # -----------------------------
    elif section == "Green Economy Reality":
        import altair as alt
        import pandas as pd
        import random

        st.markdown("<h2 style='color:#2E8B57;'>🌍 Green Economy Reality</h2>", unsafe_allow_html=True)
        st.caption("Explore how sustainable careers offer long-term financial, social, and environmental value.")
        st.markdown("---")

        # 1️⃣ Salary Comparison
        st.subheader("💰 Green Career Salary Visualizer")

        salary_df = pd.DataFrame({
            "Industry": [
                "Renewable Energy", "Sustainability Consulting", "ESG Investment",
                "Oil & Gas", "Mining", "Manufacturing"
            ],
            "Average Annual Salary (USD)": [68000, 72000, 75000, 83000, 91000, 87000],
            "Category": ["Green", "Green", "Green", "Traditional", "Traditional", "Traditional"]
        })

        chart_salary = alt.Chart(salary_df).mark_bar().encode(
            x=alt.X("Industry:N", sort=None, title="Industry"),
            y=alt.Y("Average Annual Salary (USD):Q"),
            color=alt.Color("Category:N",
                scale=alt.Scale(domain=["Green", "Traditional"], range=["#52b788", "#adb5bd"])
            ),
            tooltip=["Industry", "Average Annual Salary (USD)", "Category"]
        ).properties(height=350)

        st.altair_chart(chart_salary, use_container_width=True)

        st.info("""
        💡 *Insight:* While traditional industries may start with slightly higher salaries,
        green careers often provide faster growth, stronger stability, and global mobility.
        Professionals in renewable energy or ESG roles report higher job satisfaction and
        long-term income resilience due to expanding global regulations and innovation demand.
        """)

        st.markdown("---")

        # 2️⃣ Growth & Stability Index
        st.subheader("📈 Career Stability and Growth Index")

        roles = [
            "Renewable Energy Engineer", "ESG Analyst",
            "Circular Economy Designer", "Mining Project Manager"
        ]
        stability = [8.6, 9.1, 8.4, 4.3]
        growth = [9.3, 8.8, 9.0, 4.7]

        index_df = pd.DataFrame({"Role": roles, "Stability": stability, "Growth": growth})
        chart_index = alt.Chart(index_df.melt("Role")).mark_line(point=True).encode(
            x="Role:N",
            y="value:Q",
            color="variable:N",
            tooltip=["Role", "value", "variable"]
        ).properties(height=350)

        st.altair_chart(chart_index, use_container_width=True)
        st.success("""
        📊 Green professions consistently demonstrate higher stability and growth scores
        due to policy incentives, technological integration, and long-term societal demand.
        """)

        st.markdown("---")

        # 3️⃣ ROI Calculator
        st.subheader("📊 Green ROI (Return on Impact) Calculator")

        col1, col2, col3 = st.columns(3)
        with col1:
            career = st.selectbox(
                "Choose a Green Career",
                ["ESG Analyst", "Renewable Engineer", "Climate Policy Advisor", "Sustainability Data Specialist"]
            )
        with col2:
            years = st.slider("Years of Experience", 1, 10, 3)
        with col3:
            skill_level = st.select_slider("Skill Level", ["Beginner", "Intermediate", "Advanced"])

        base_income = {
            "ESG Analyst": 70000,
            "Renewable Engineer": 72000,
            "Climate Policy Advisor": 68000,
            "Sustainability Data Specialist": 74000
        }
        impact_factor = {"Beginner": 1.1, "Intermediate": 1.3, "Advanced": 1.6}

        roi = int(base_income[career] * impact_factor[skill_level] * (1 + (years * 0.07)))
        st.metric("💵 Estimated 5-Year ROI (USD)", f"{roi:,}")
        st.caption("Includes both financial growth and environmental impact value estimation over 5 years.")
        st.markdown("---")

        # 4️⃣ Real Voices
        st.subheader("🎤 Real Voices from the Field")

        stories = [
            {
                "name": "🌱 Lina — From Finance to ESG Investing",
                "story": "After 5 years in corporate finance, Lina transitioned into ESG investing. She discovered that sustainable portfolios outperform in market resilience and provide stronger personal fulfillment."
            },
            {
                "name": "🔋 Arjun — Energy Engineer Turned Innovator",
                "story": "Arjun left a mining project to work on solar microgrids in rural Indonesia. His income stabilized, and his work now powers 4,000 homes sustainably."
            },
            {
                "name": "🌾 Mei — Circular Designer in Manufacturing",
                "story": "Mei joined a circular design lab focusing on zero-waste production. Her creative freedom and industry recognition grew faster than any past corporate role."
            }
        ]

        for s in stories:
            with st.expander(s["name"], expanded=False):
                st.write(s["story"])
                st.caption("💬 Each story demonstrates how passion for sustainability aligns with both career growth and social value.")

        st.markdown("---")


        # 5️⃣ Future Green Career Trends (2035 Outlook)
        st.subheader("🔮 Future Green Career Trends 2035")

        st.caption("A forward look into how sustainable careers will transform over the next decade.")

        # Simulated data for visualization
        trend_data = pd.DataFrame({
            "Year": list(range(2025, 2036)),
            "Renewable Energy": [45, 48, 52, 57, 63, 70, 78, 86, 92, 97, 100],
            "Circular Economy": [30, 35, 42, 50, 59, 69, 80, 89, 94, 98, 100],
            "Climate Tech": [20, 25, 33, 45, 55, 68, 78, 90, 97, 99, 100],
            "ESG Analytics": [25, 30, 38, 47, 56, 64, 74, 83, 91, 96, 100]
        })

        # Melt for Altair
        trend_df = trend_data.melt("Year", var_name="Sector", value_name="Growth Index")

        # Create growth line chart
        chart_trend = alt.Chart(trend_df).mark_line(point=True).encode(
            x=alt.X("Year:O"),
            y=alt.Y("Growth Index:Q", title="Relative Growth Index (2025=Base)"),
            color=alt.Color("Sector:N", scale=alt.Scale(scheme="greens")),
            tooltip=["Sector", "Year", "Growth Index"]
        ).properties(height=350)

        st.altair_chart(chart_trend, use_container_width=True)

        st.info("""
        🌱 *Insight:*  
        Between 2025 and 2035, the **fastest-growing green sectors** will include Climate Tech,
        ESG Analytics, and Renewable Energy.  
        The demand for data-driven sustainability professionals, circular design thinkers,
        and climate innovators will expand dramatically as governments and industries align with
        net-zero targets and global green financing standards.
        """)

        # Regional focus text (no chart, for smoother performance)
        st.success("""
        🌏 *Regional Outlook:*  
        By 2035, **Southeast Asia** is projected to become a global hub for sustainable innovation.
        Cities like **Singapore**, **Jakarta**, and **Ho Chi Minh City** will lead in renewable manufacturing,
        while emerging economies such as **Vietnam** and **Philippines** will specialize in green digital services
        and eco-infrastructure startups.  
        The youth generation will play a critical role in driving these transitions.
        """)

        # Closing message
        st.caption("📈 Use these insights to align your learning and career path toward future-proof green opportunities.")
        st.markdown("---")

        # 5️⃣ Closing Insight
        st.info("""
        🌍 The future economy rewards resilience, creativity, and systems thinking.
        Green industries are not just about environmental protection—they represent
        the next frontier of innovation, profitability, and purpose-driven work.
        """)

        


