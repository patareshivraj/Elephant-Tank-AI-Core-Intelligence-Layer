import logging
from typing import List, Dict, Any
from app.semantic.vector_store import VectorStore

logger = logging.getLogger("ElephantTank.Semantic.IndexManager")

MOCK_INVESTORS = [
    {
        "id": "inv_seq_deeptech",
        "name": "Horizon Venture Partners",
        "description": "Enterprise venture capital firm investing in Series A deeptech, SaaS, cloud infrastructure, and core artificial intelligence innovations.",
        "metadata": {
            "name": "Horizon Venture Partners",
            "stages": ["Series A", "Series B"],
            "industries": ["Deeptech", "SaaS", "AI", "Cloud Infrastructure"],
            "min_check": 3000000,
            "max_check": 15000000,
            "ideal_stage": "Series A"
        }
    },
    {
        "id": "inv_first_seed",
        "name": "Spark Seed Ventures",
        "description": "Pre-seed and Seed stage fund backing high-potential developers and first-time founders in developer tools, generative AI applications, and consumer platforms.",
        "metadata": {
            "name": "Spark Seed Ventures",
            "stages": ["Pre-seed", "Seed"],
            "industries": ["Developer Tools", "AI Applications", "Consumer Tech"],
            "min_check": 250000,
            "max_check": 1500000,
            "ideal_stage": "Seed"
        }
    },
    {
        "id": "inv_yc_style",
        "name": "Antigravity Accelerator",
        "description": "Global accelerator providing pre-seed investment, intensive mentoring, and validation checks for early-stage AI, web3, SaaS, and hardware projects.",
        "metadata": {
            "name": "Antigravity Accelerator",
            "stages": ["Pre-seed"],
            "industries": ["AI", "Web3", "SaaS", "Hardware", "BioTech"],
            "min_check": 100000,
            "max_check": 500000,
            "ideal_stage": "Pre-seed"
        }
    },
    {
        "id": "inv_bio_health",
        "name": "Aegis Healthcare Capital",
        "description": "Specialized healthtech VC targeting FDA-cleared diagnostics, computer vision imaging, therapeutics, and biomedical AI systems at Seed and Series A stages.",
        "metadata": {
            "name": "Aegis Healthcare Capital",
            "stages": ["Seed", "Series A"],
            "industries": ["Healthcare", "Healthtech", "AI Diagnostics", "Biotech"],
            "min_check": 1000000,
            "max_check": 8000000,
            "ideal_stage": "Series A"
        }
    },
    {
        "id": "inv_fin_alpha",
        "name": "Stripe-Style Fintech Partners",
        "description": "Fintech focused seed-to-series-A fund supporting billing engine infrastructures, transaction ledgers, digital banks, and payment orchestration software.",
        "metadata": {
            "name": "Stripe-Style Fintech Partners",
            "stages": ["Seed", "Series A"],
            "industries": ["Fintech", "Financial Infrastructure", "Payments", "SaaS"],
            "min_check": 500000,
            "max_check": 4000000,
            "ideal_stage": "Seed"
        }
    }
]

MOCK_MENTORS = [
    {
        "id": "men_vance_health",
        "name": "Dr. Elizabeth Vance",
        "description": "Ex-Harvard Medical School MD, Chief Medical Officer at AI Health Corp. Expert in FDA clearances, clinical validation trials, and computer vision MRI analytics.",
        "metadata": {
            "name": "Dr. Elizabeth Vance",
            "specialization": "Clinical validation, FDA regulation, Healthcare AI",
            "industries": ["Healthcare", "Healthtech", "AI Diagnostics", "Biotech"],
            "compatible_stages": ["Seed", "Series A"],
            "technical": True
        }
    },
    {
        "id": "men_sanjay_fintech",
        "name": "Sanjay Patel",
        "description": "Serial Fintech founder, exited transaction billing engine 'LedgerPay' to Visa. Expert in credit cards scaling, enterprise sales, regulatory payments compliance, and SaaS ARR scaling.",
        "metadata": {
            "name": "Sanjay Patel",
            "specialization": "ARR scaling, payments infra, compliance, B2B sales",
            "industries": ["Fintech", "Financial Infrastructure", "Payments", "SaaS"],
            "compatible_stages": ["Pre-seed", "Seed", "Series A"],
            "technical": False
        }
    },
    {
        "id": "men_marina_infra",
        "name": "Marina Kovalenko",
        "description": "Core Infrastructure Lead at Vercel. Veteran developer specializing in distributed systems high-scalability, AWS serverless database pipelines, Kubernetes clustering, and high-performance Rust web frameworks.",
        "metadata": {
            "name": "Marina Kovalenko",
            "specialization": "Distributed systems, scalability, Kubernetes, Cloud architectures",
            "industries": ["Deeptech", "Developer Tools", "AI", "Cloud Infrastructure"],
            "compatible_stages": ["Seed", "Series A", "Series B"],
            "technical": True
        }
    },
    {
        "id": "men_david_growth",
        "name": "David Chen",
        "description": "Ex-VP Growth at Slack and Miro. Product growth architect specialized in product-led growth (PLG) mechanics, marketing acquisition channels, viral feedback loops, and customer conversion funnels.",
        "metadata": {
            "name": "David Chen",
            "specialization": "Product-led growth, PLG marketing, SaaS conversion funnels",
            "industries": ["SaaS", "Consumer Tech", "DevTools", "AI Applications"],
            "compatible_stages": ["Seed", "Series A"],
            "technical": False
        }
    }
]

class IndexManager:
    @classmethod
    def seed_ecosystem_if_empty(cls):
        """
        Populates high-fidelity mock investors and mentors into vector index collections if empty.
        """
        # Seed Investors
        inv_col = VectorStore.get_collection("investors")
        if not inv_col.get() or len(inv_col.get().get("ids", [])) == 0:
            logger.info("Seeding Vector DB with mock venture investors...")
            for inv in MOCK_INVESTORS:
                VectorStore.upsert_item("investors", inv["id"], inv["description"], inv["metadata"])
                
        # Seed Mentors
        men_col = VectorStore.get_collection("mentors")
        if not men_col.get() or len(men_col.get().get("ids", [])) == 0:
            logger.info("Seeding Vector DB with mock ecosystem mentors...")
            for men in MOCK_MENTORS:
                VectorStore.upsert_item("mentors", men["id"], men["description"], men["metadata"])

    @classmethod
    def index_startup(cls, startup_id: str, structured_data: Dict[str, Any]):
        """
        Indexes standard normalized startup data into 'startups' namespace.
        """
        # Construct single cohesive document containing semantic info
        name = structured_data.get("startup_name", "Unknown Startup")
        desc = structured_data.get("startup_description", "")
        stage = structured_data.get("target_stage", "Seed")
        founder = structured_data.get("founder_data", "")
        
        index_doc = f"Startup: {name}\nStage: {stage}\nDescription: {desc}\nFounder Team: {founder}"
        
        metadata = {
            "startup_name": name,
            "target_stage": stage,
            "has_founder_data": bool(founder.strip())
        }
        
        VectorStore.upsert_item("startups", startup_id, index_doc, metadata)
        logger.info(f"Indexed startup '{name}' ({startup_id}) successfully.")

    @classmethod
    def reset_all_indices(cls):
        """
        Clears all databases and collections.
        """
        client = VectorStore.get_client()
        for name in ["startups", "investors", "mentors"]:
            try:
                client.delete_collection(name)
                logger.info(f"Dropped collection '{name}'")
            except Exception:
                pass
        cls.seed_ecosystem_if_empty()
