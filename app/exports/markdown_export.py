import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Exports.MarkdownExport")

class MarkdownExportManager:
    """
    Markdown Export Module.
    Formulates compiled strategic reports into a premium, investor-grade Markdown output.
    """
    
    @classmethod
    def generate_markdown(cls, report_data: Dict[str, Any]) -> str:
        """
        Converts the compiled master report dict into a high-fidelity Markdown string.
        """
        logger.info("Generating premium Markdown report...")
        profile = report_data.get("startup_profile", {})
        memo = report_data.get("investment_memo", {})
        founder = report_data.get("founder_intelligence", {})
        risks = report_data.get("risk_analysis", {})
        positioning = report_data.get("market_positioning", {})
        opp = report_data.get("ecosystem_opportunity", {})
        recs = report_data.get("prioritized_recommendations", [])
        
        md = []
        md.append("# ELEPHANT TANK AI - MASTER VENTURE INTELLIGENCE REPORT")
        md.append("---")
        md.append(f"**Startup Name:** {profile.get('startup_name', 'N/A')}  ")
        md.append(f"**Target Stage:** {profile.get('target_stage', 'N/A')}  ")
        md.append(f"**Overall Score:** `{profile.get('overall_score', 0)}/100`  ")
        md.append(f"**Funding Readiness Level:** `{profile.get('funding_readiness_level', 'N/A')}`  ")
        md.append(f"**Pipeline Run:** `{report_data.get('pipeline_id', 'N/A')}`  ")
        md.append("")
        
        md.append("## 1. INSTITUTIONAL INVESTMENT MEMO")
        md.append(f"> **Investment Thesis Verdict:** {memo.get('analyst_verdict', 'N/A')}")
        md.append("")
        md.append(f"### Investment Thesis")
        md.append(f"{memo.get('investment_thesis', 'N/A')}")
        md.append("")
        md.append("### Market Opportunity & Timing")
        md.append(f"{memo.get('market_opportunity_analysis', 'N/A')}")
        md.append("")
        md.append("### Defensibility & Competitive Landscape")
        md.append(f"{memo.get('defensibility_and_competition_summary', 'N/A')}")
        md.append("")
        
        md.append("## 2. FOUNDER OPERATIONAL PASS_PORT")
        md.append(f"- **Execution Readiness:** `{founder.get('execution_readiness_level', 'N/A')}`")
        md.append(f"- **Technical Capability Rating:** `{founder.get('technical_capability_rating', 'N/A')}`")
        md.append(f"- **Operating Potential Index:** `{founder.get('operating_potential_index', 0.0)}/10.0`")
        md.append("")
        md.append("### Operational Capability Summary")
        md.append(f"{founder.get('operational_capability_narrative', 'N/A')}")
        md.append("")
        md.append("### Strengths Profile")
        for st in founder.get("strengths_summary", []):
            md.append(f"- ✅ {st}")
        md.append("")
        
        md.append("## 3. RISK INTELLIGENCE MATRIX")
        md.append(f"**Risk Profile Assessment:** `{risks.get('overall_risk_profile', 'N/A')}` (High-Severity Risks: {risks.get('high_severity_risks_count', 0)})  ")
        md.append(f"**Average Risk Assessment Confidence:** `{risks.get('average_risk_confidence', 0)}/10`  ")
        md.append("")
        md.append("| Risk Domain | Observed Risk Description | Severity | Confidence | Mitigation Recommendation |")
        md.append("| :--- | :--- | :--- | :--- | :--- |")
        for entry in risks.get("classified_risks", []):
            md.append(f"| **{entry['risk_domain']}** | {entry['description']} | `{entry['severity']}` | {entry['confidence_level']}/10 | {entry['mitigation_recommendation']} |")
        md.append("")
        
        md.append("## 4. MARKET POSITIONING & DEFENSIBILITY ANALYSIS")
        md.append(f"- **Market Saturation Level:** `{positioning.get('market_saturation', 'N/A')}`")
        md.append(f"- **Defensibility Rating:** `{positioning.get('defensibility_rating', 'N/A')}`")
        md.append(f"- **Differentiation Index:** `{positioning.get('differentiation_index', 0.0)}/10.0`")
        md.append(f"- **Market Timing Fit:** `{positioning.get('market_timing_fit', 'N/A')}`")
        md.append("")
        md.append("### Competitive Positioning Summary")
        md.append(f"{positioning.get('competitive_positioning_narrative', 'N/A')}")
        md.append("")
        md.append("### Category Overlap Warnings")
        for warning in positioning.get("category_overlap_warning", []):
            md.append(f"- ⚠️ {warning}")
        md.append("")
        
        md.append("## 5. ECOSYSTEM OPPORTUNITY & EXPANSION PATHS")
        md.append(f"### Underserved Market Opportunity")
        md.append(f"{opp.get('underserved_market_opportunity', 'N/A')}")
        md.append("")
        md.append("### Adjacent Market Expansion Candidates")
        for cand in opp.get("adjacent_market_possibilities", []):
            md.append(f"- 🌐 {cand}")
        md.append("")
        md.append("### Core Strategic Opportunity Summary")
        md.append(f"{opp.get('strategic_opportunity_summary', 'N/A')}")
        md.append("")
        
        md.append("## 6. PRIORITIZED STRATEGIC RECOMMENDATIONS")
        md.append("> Recommendations are deterministically ranked starting with critical founder risks first, existential market threats, and execution blockers.")
        md.append("")
        for idx, rec in enumerate(recs):
            md.append(f"### #{idx+1} [{rec['category']}] {rec['title']}")
            md.append(f"**Description:** {rec['description']}  ")
            md.append(f"**Mitigation Action Plan:** *{rec['mitigation_action']}*")
            md.append("")
            
        md.append("---")
        md.append("*Elephant Tank AI - Deterministic Startup Intelligence & Venture Due Diligence Engine*")
        
        return "\n".join(md)

    @classmethod
    def export_to_markdown(cls, report_data: Dict[str, Any], output_path: str) -> str:
        """
        Generates and saves the markdown report file.
        """
        logger.info(f"Exporting strategic report to Markdown: {output_path}")
        try:
            content = cls.generate_markdown(report_data)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Markdown export completed successfully.")
            return output_path
        except Exception as e:
            logger.error(f"Failed to export to Markdown: {e}")
            raise
