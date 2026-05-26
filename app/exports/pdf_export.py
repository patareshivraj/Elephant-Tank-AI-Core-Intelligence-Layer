import logging
import fitz  # PyMuPDF
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Exports.PDFExport")

class PDFExportManager:
    """
    PDF Export Module.
    Uses PyMuPDF to paint professional, investor-grade venture reports directly to PDF files.
    Enforces a strict offline-stable compilation architecture.
    """
    
    @classmethod
    def export_to_pdf(cls, report_data: Dict[str, Any], output_path: str) -> str:
        """
        Paints structured report onto high-fidelity PDF pages.
        """
        logger.info(f"Exporting strategic report to PDF: {output_path}")
        try:
            profile = report_data.get("startup_profile", {})
            memo = report_data.get("investment_memo", {})
            founder = report_data.get("founder_intelligence", {})
            risks = report_data.get("risk_analysis", {})
            positioning = report_data.get("market_positioning", {})
            opp = report_data.get("ecosystem_opportunity", {})
            recs = report_data.get("prioritized_recommendations", [])
            
            doc = fitz.open()
            
            # --- PAGE 1: TITLE & INVESTMENT THESIS ---
            page = doc.new_page(width=595, height=842)  # Standard A4 size
            
            # Draw header banner
            page.draw_rect(fitz.Rect(30, 30, 565, 80), color=(0.1, 0.2, 0.4), fill=(0.1, 0.2, 0.4))
            page.insert_text(fitz.Point(45, 62), "ELEPHANT TANK AI - MASTER VENTURE REPORT", fontsize=16, color=(1, 1, 1))
            
            # Metadata Box
            y = 110
            page.insert_text(fitz.Point(40, y), f"Startup Name: {profile.get('startup_name')}", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
            page.insert_text(fitz.Point(40, y+20), f"Target Stage: {profile.get('target_stage')}", fontsize=11, fontname="helv")
            page.insert_text(fitz.Point(300, y), f"Overall Score: {profile.get('overall_score')}/100", fontsize=11, fontname="hebo")
            page.insert_text(fitz.Point(300, y+20), f"Readiness: {profile.get('funding_readiness_level')}", fontsize=11, fontname="helv")
            
            # Draw line divider
            page.draw_line(fitz.Point(40, y+35), fitz.Point(555, y+35), color=(0.7, 0.7, 0.7))
            
            # Memo Section
            y_memo = y + 55
            page.insert_text(fitz.Point(40, y_memo), "1. VC Investment Memo & Thesis", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.4))
            
            # Thesis Textbox
            thesis_rect = fitz.Rect(40, y_memo + 15, 555, y_memo + 90)
            page.draw_rect(thesis_rect, color=(0.9, 0.9, 0.9), fill=(0.95, 0.95, 0.95))
            page.insert_textbox(thesis_rect, f"Verdict: {memo.get('analyst_verdict')}\n\n{memo.get('investment_thesis')}", fontsize=9, fontname="helv")
            
            # Market Opportunity Textbox
            opp_title_y = y_memo + 110
            page.insert_text(fitz.Point(40, opp_title_y), "Market Opportunity & Saturation Analysis", fontsize=11, fontname="hebo")
            opp_rect = fitz.Rect(40, opp_title_y + 10, 555, opp_title_y + 90)
            page.insert_textbox(opp_rect, memo.get('market_opportunity_analysis', ''), fontsize=9, fontname="helv")
            
            # Competitive Positioning Textbox
            comp_title_y = opp_title_y + 110
            page.insert_text(fitz.Point(40, comp_title_y), "Competitive Defensibility Strategy", fontsize=11, fontname="hebo")
            comp_rect = fitz.Rect(40, comp_title_y + 10, 555, comp_title_y + 90)
            page.insert_textbox(comp_rect, memo.get('defensibility_and_competition_summary', ''), fontsize=9, fontname="helv")
            
            # Draw footer
            page.insert_text(fitz.Point(40, 815), "Page 1 - Confidential Due Diligence", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
            
            # --- PAGE 2: FOUNDER & RISK MATRIX ---
            page2 = doc.new_page(width=595, height=842)
            page2.insert_text(fitz.Point(40, 50), "2. Founder Intelligence Passport", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.4))
            
            # Founder Grid
            fy = 70
            page2.insert_text(fitz.Point(40, fy), f"Execution Readiness: {founder.get('execution_readiness_level')}", fontsize=10, fontname="helv")
            page2.insert_text(fitz.Point(40, fy+15), f"Technical Capability: {founder.get('technical_capability_rating')}", fontsize=10, fontname="helv")
            page2.insert_text(fitz.Point(300, fy), f"Operating Index: {founder.get('operating_potential_index')}/10.0", fontsize=10, fontname="hebo")
            
            founder_rect = fitz.Rect(40, fy+30, 555, fy+110)
            page2.insert_textbox(founder_rect, founder.get('operational_capability_narrative', ''), fontsize=9, fontname="helv")
            
            # Risks Section
            ry = fy + 130
            page2.insert_text(fitz.Point(40, ry), "3. Risk Intelligence Assessment Matrix", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.4))
            page2.insert_text(fitz.Point(40, ry+15), f"Overall Risk Profile: {risks.get('overall_risk_profile')}  |  Average Confidence: {risks.get('average_risk_confidence')}/10", fontsize=9, fontname="hebo")
            
            # Paint risks box list
            risk_y_cursor = ry + 30
            for idx, r in enumerate(risks.get("classified_risks", [])):
                box_rect = fitz.Rect(40, risk_y_cursor, 555, risk_y_cursor + 45)
                page2.draw_rect(box_rect, color=(0.8, 0.8, 0.8), fill=(0.98, 0.98, 0.98))
                text_content = f"[{r['risk_domain']}] Severity: {r['severity']}  (Confidence: {r['confidence_level']}/10)\nDescription: {r['description']}\nMitigation: {r['mitigation_recommendation']}"
                page2.insert_textbox(box_rect, text_content, fontsize=8, fontname="helv")
                risk_y_cursor += 50
                
            page2.insert_text(fitz.Point(40, 815), "Page 2 - Confidential Due Diligence", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
            
            # --- PAGE 3: RECOMMENDATIONS & ECOSYSTEM ---
            page3 = doc.new_page(width=595, height=842)
            page3.insert_text(fitz.Point(40, 50), "4. Ecosystem Opportunity & Strategic Outlook", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.4))
            
            oy = 70
            opp_box = fitz.Rect(40, oy, 555, oy+70)
            page3.draw_rect(opp_box, color=(0.9, 0.9, 0.9))
            page3.insert_textbox(opp_box, f"Underserved Opportunity: {opp.get('underserved_market_opportunity')}\n\nStrategic Path: {opp.get('strategic_opportunity_summary')}", fontsize=9, fontname="helv")
            
            # Recommendations
            recy = oy + 95
            page3.insert_text(fitz.Point(40, recy), "5. Prioritized Strategic Recommendations (Founder & Market Risks First)", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.4))
            
            rec_cursor = recy + 20
            for idx, rec in enumerate(recs[:4]): # Top 4 prioritized recommendations
                rec_box = fitz.Rect(40, rec_cursor, 555, rec_cursor + 48)
                page3.draw_rect(rec_box, color=(0.1, 0.2, 0.4), fill=(0.95, 0.97, 1.0))
                rec_text = f"#{idx+1} [{rec['category']}] Priority: {rec['priority_score']} - {rec['title']}\nDescription: {rec['description']}\nAction Plan: {rec['mitigation_action']}"
                page3.insert_textbox(rec_box, rec_text, fontsize=8, fontname="helv")
                rec_cursor += 54
                
            page3.insert_text(fitz.Point(40, 815), "Page 3 - Confidential Due Diligence", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
            
            doc.save(output_path)
            doc.close()
            logger.info("PDF export completed successfully.")
            return output_path
        except Exception as e:
            logger.error(f"Failed to export to PDF: {e}")
            raise
