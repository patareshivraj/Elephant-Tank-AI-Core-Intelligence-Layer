import sys
import os
import json

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.reporting.executive_report import ExecutiveReportGenerator
from app.exports.json_export import JSONExportManager
from app.exports.markdown_export import MarkdownExportManager
from app.exports.pdf_export import PDFExportManager

def test_report_quality_and_exports():
    print("========================================")
    print(" ELEPHANT TANK - REPORT QUALITY TESTER")
    print("========================================")
    
    # 1. Setup Mock Evaluation Response
    mock_eval = {
        "pipeline_id": "test_pipeline_xyz",
        "startup_profile": {
            "startup_name": "Sovereign Health",
            "target_stage": "Series A"
        },
        "evaluation_results": {
            "overall_score": 72,
            "innovation_score": 7,
            "market_score": 8,
            "scalability_score": 6,
            "founder_score": 7,
            "funding_readiness_score": 7
        },
        "founder_intelligence": {
            "strengths": ["Strong clinical credentials", "Prior medical exit history"],
            "weaknesses": ["Lack of mature in-house enterprise sales execution experience"]
        },
        "risk_analysis": {
            "risks": [
                "Founder Team: Executive gap in B2B enterprise sales hires.",
                "Regulatory: FDA registration hurdles on core software product.",
                "Competitive: Emerging competitors are expanding SaaS feature sets."
            ]
        },
        "recommendations": [
            "Founder Talent: Hire an experienced B2B medical enterprise sales head.",
            "Market Strategy: Address severe GTM saturation with pricing optimizations.",
            "Regulatory Clearances: Set up FDA pre-compliance registry logs immediately."
        ],
        "due_diligence_questions": [
            "How do you plan to shorten corporate hospital enterprise sales cycles?",
            "What is the current technical roadmap for FDA pre-compliance logs?"
        ]
    }
    
    # 2. Compile Master Orchestrated Report
    print("[1] Compiling Master Executive Report...")
    master = ExecutiveReportGenerator.generate_executive_report(
        mock_eval,
        raw_description="Sovereign Health builds FDA-compliant enterprise software that helps hospital networks automate EHR clinical charting workflows.",
        raw_founder_data="Dr. Sarah Jenkins, former Medical Director at Johns Hopkins Healthcare. MD/PhD."
    )
    
    # Verify section keys exist
    assert "pipeline_id" in master
    assert "startup_profile" in master
    assert "investment_memo" in master
    assert "founder_intelligence" in master
    assert "risk_analysis" in master
    assert "market_positioning" in master
    assert "ecosystem_opportunity" in master
    assert "prioritized_recommendations" in master
    assert "due_diligence_questions" in master
    assert "execution_logs" in master
    
    print("[SUCCESS] All 10 master report sections are fully initialized!")
    
    # 3. Setup Temp Export Paths
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "test_reports"))
    os.makedirs(temp_dir, exist_ok=True)
    
    json_path = os.path.join(temp_dir, "test_report.json")
    md_path = os.path.join(temp_dir, "test_report.md")
    pdf_path = os.path.join(temp_dir, "test_report.pdf")
    
    print("\n[2] Triggering Multi-Format Exports...")
    JSONExportManager.export_to_json(master, json_path)
    MarkdownExportManager.export_to_markdown(master, md_path)
    PDFExportManager.export_to_pdf(master, pdf_path)
    
    # Verify file sizes are greater than 0
    assert os.path.exists(json_path) and os.path.getsize(json_path) > 0, "JSON export is missing or empty."
    assert os.path.exists(md_path) and os.path.getsize(md_path) > 0, "Markdown export is missing or empty."
    assert os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0, "PDF export is missing or empty."
    
    print(f"  [OK] JSON Export size: {os.path.getsize(json_path)} bytes")
    print(f"  [OK] Markdown Export size: {os.path.getsize(md_path)} bytes")
    print(f"  [OK] PDF Export size: {os.path.getsize(pdf_path)} bytes")
    
    # Clean up files
    os.remove(json_path)
    os.remove(md_path)
    os.remove(pdf_path)
    os.rmdir(temp_dir)
    
    print("\n[SUCCESS] MULTI-FORMAT REPORT EXPORTS COMPLETED AND VALIDATED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_report_quality_and_exports()
    except Exception as e:
        print(f"\n[FAIL] Test suite failed: {e}")
        sys.exit(1)
