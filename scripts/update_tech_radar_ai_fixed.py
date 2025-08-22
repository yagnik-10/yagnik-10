#!/usr/bin/env python3
"""
AI-Enhanced Tech Radar Auto-Updater (Fixed Version)
Uses free AI models with better compatibility handling
"""

import json
import re
import requests
import pathlib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np
from collections import Counter
import pickle

# AI/ML Libraries with better error handling
AI_AVAILABLE = False
AI_MODELS = {}

try:
    # Try to import AI libraries with specific versions
    import torch
    print(f"✅ PyTorch version: {torch.__version__}")
    
    # Try sentence transformers with fallback
    try:
        from sentence_transformers import SentenceTransformer
        AI_MODELS['sentence_transformer'] = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Sentence Transformer loaded successfully")
    except Exception as e:
        print(f"⚠️ Sentence Transformer failed: {e}")
        # Fallback to simpler embedding method
        AI_MODELS['simple_embeddings'] = True
    
    # Try sklearn
    try:
        from sklearn.cluster import KMeans
        from sklearn.metrics.pairwise import cosine_similarity
        AI_MODELS['sklearn'] = True
        print("✅ Scikit-learn loaded successfully")
    except Exception as e:
        print(f"⚠️ Scikit-learn failed: {e}")
    
    # Try NLTK
    try:
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        from nltk.sentiment import SentimentIntensityAnalyzer
        AI_MODELS['sentiment'] = SentimentIntensityAnalyzer()
        print("✅ NLTK sentiment analyzer loaded successfully")
    except Exception as e:
        print(f"⚠️ NLTK failed: {e}")
    
    # Try spaCy
    try:
        import spacy
        AI_MODELS['spacy'] = spacy.load('en_core_web_sm')
        print("✅ spaCy loaded successfully")
    except Exception as e:
        print(f"⚠️ spaCy failed: {e}")
    
    # If we have at least some AI capabilities, mark as available
    if len(AI_MODELS) > 0:
        AI_AVAILABLE = True
        print(f"🤖 AI models available: {list(AI_MODELS.keys())}")
    
except ImportError as e:
    print(f"⚠️ AI libraries not available: {e}")

class AITechRadarUpdaterFixed:
    def __init__(self):
        self.root = pathlib.Path(__file__).resolve().parents[1]
        self.readme_path = self.root / "README.md"
        self.tech_data_path = self.root / "data" / "tech_trends_ai_fixed.json"
        self.config_path = self.root / "data" / "tech_radar_config.json"
        
        # Load configuration
        self.config = self.load_config()
        
        # Tech radar categories
        self.categories = ["adopt", "trial", "assess", "avoid"]
        
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return {}
    
    def simple_embedding(self, text: str) -> List[float]:
        """Simple embedding method as fallback when transformers fail"""
        # Create a simple bag-of-words embedding
        words = text.lower().split()
        # Simple frequency-based embedding (very basic but works)
        word_freq = Counter(words)
        # Normalize to unit vector
        total = sum(word_freq.values())
        if total == 0:
            return [0.0] * 100
        return [word_freq.get(f"word_{i}", 0) / total for i in range(100)]
    
    def simple_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0.0
    
    def fetch_github_trends(self) -> List[Dict]:
        """Fetch trending repositories from GitHub with enhanced data"""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": "created:>2024-01-01 stars:>100",
                "sort": "stars",
                "order": "desc",
                "per_page": 100
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                repos = response.json()["items"]
                enhanced_repos = []
                
                for repo in repos:
                    if repo["language"] and repo["description"]:
                        repo_data = {
                            "name": repo["name"],
                            "description": repo["description"],
                            "language": repo["language"],
                            "stars": repo["stargazers_count"],
                            "forks": repo["forks_count"],
                            "url": repo["html_url"],
                            "created_at": repo["created_at"],
                            "updated_at": repo["updated_at"],
                            "topics": repo.get("topics", []),
                            "full_name": repo["full_name"]
                        }
                        
                        # Enhanced categorization
                        repo_data["ai_category"] = self.categorize_tech_enhanced(repo_data)
                        repo_data["sentiment_score"] = self.analyze_sentiment_enhanced(repo_data["description"])
                        repo_data["relevance_score"] = self.calculate_relevance_enhanced(repo_data)
                        
                        enhanced_repos.append(repo_data)
                
                return enhanced_repos
                
        except Exception as e:
            print(f"Error fetching GitHub trends: {e}")
        
        return []
    
    def fetch_stackoverflow_trends(self) -> List[Dict]:
        """Fetch trending technologies from Stack Overflow"""
        try:
            url = "https://api.stackexchange.com/2.3/tags"
            params = {
                "order": "desc",
                "sort": "popular",
                "site": "stackoverflow",
                "pagesize": 50
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                tags = response.json()["items"]
                enhanced_tags = []
                
                for tag in tags:
                    tag_data = {
                        "name": tag["name"],
                        "count": tag["count"],
                        "description": f"Popular {tag['name']} technology with {tag['count']} questions"
                    }
                    
                    # Enhanced categorization
                    tag_data["ai_category"] = self.categorize_tech_enhanced(tag_data)
                    tag_data["sentiment_score"] = self.analyze_sentiment_enhanced(tag_data["description"])
                    tag_data["relevance_score"] = self.calculate_relevance_enhanced(tag_data)
                    
                    enhanced_tags.append(tag_data)
                
                return enhanced_tags
                
        except Exception as e:
            print(f"Error fetching Stack Overflow trends: {e}")
        
        return []
    
    def fetch_all_trends(self) -> List[Dict]:
        """Fetch and combine trends from all sources"""
        github_trends = self.fetch_github_trends()
        stackoverflow_trends = self.fetch_stackoverflow_trends()
        
        # Combine and deduplicate trends
        all_trends = github_trends + stackoverflow_trends
        unique_trends = []
        seen_names = set()
        
        for trend in all_trends:
            if trend["name"] not in seen_names:
                unique_trends.append(trend)
                seen_names.add(trend["name"])
        
        return unique_trends
    
    def categorize_tech_enhanced(self, tech_data: Dict) -> str:
        """Enhanced tech categorization with fallback methods"""
        text = f"{tech_data['name']} {tech_data.get('description', '')} {tech_data.get('language', '')}".lower()
        
        # Define category keywords
        category_keywords = {
            "adopt": [
                "production", "stable", "mature", "enterprise", "production-ready",
                "battle-tested", "widely-adopted", "industry-standard"
            ],
            "trial": [
                "experimental", "beta", "alpha", "new", "innovative", "promising",
                "cutting-edge", "next-generation", "revolutionary"
            ],
            "assess": [
                "monitoring", "evaluating", "considering", "potential", "emerging",
                "trending", "growing", "developing"
            ],
            "avoid": [
                "deprecated", "outdated", "legacy", "security-issue", "performance-problem",
                "abandoned", "discontinued", "vulnerable"
            ]
        }
        
        # Calculate scores for each category
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        # Return category with highest score, default to assess
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        else:
            return "assess"
    
    def ai_categorize_tech(self, tech_data: Dict) -> str:
        """AI-powered categorization with fallback"""
        if not AI_AVAILABLE:
            return "assess"
        
        try:
            text = f"{tech_data['name']} {tech_data.get('description', '')} {tech_data.get('language', '')}"
            
            # Use sentence transformer if available
            if 'sentence_transformer' in AI_MODELS:
                embedding = AI_MODELS['sentence_transformer'].encode([text])
                
                # Define category embeddings
                category_texts = {
                    "adopt": "production ready mature widely adopted stable enterprise",
                    "trial": "experimental promising new innovative beta",
                    "assess": "monitoring evaluating considering potential",
                    "avoid": "deprecated outdated security issues performance problems"
                }
                
                similarities = {}
                for category, cat_text in category_texts.items():
                    cat_embedding = AI_MODELS['sentence_transformer'].encode([cat_text])
                    if 'sklearn' in AI_MODELS:
                        similarity = cosine_similarity(embedding, cat_embedding)[0][0]
                        similarities[category] = similarity
                    else:
                        # Fallback to simple similarity
                        similarities[category] = self.simple_similarity(text, cat_text)
                
                return max(similarities, key=similarities.get)
            
            # Fallback to enhanced categorization (not recursive)
            return self.categorize_tech_enhanced(tech_data)
            
        except Exception as e:
            print(f"Error in AI categorization: {e}")
            return "assess"
    
    def analyze_sentiment_enhanced(self, text: str) -> float:
        """Enhanced sentiment analysis with fallback"""
        if not AI_AVAILABLE or 'sentiment' not in AI_MODELS:
            # Simple sentiment analysis based on keywords
            positive_words = ['fast', 'efficient', 'powerful', 'modern', 'secure', 'scalable', 'reliable']
            negative_words = ['slow', 'buggy', 'deprecated', 'outdated', 'vulnerable', 'broken']
            
            text_lower = text.lower()
            positive_score = sum(1 for word in positive_words if word in text_lower)
            negative_score = sum(1 for word in negative_words if word in text_lower)
            
            total = positive_score + negative_score
            if total == 0:
                return 0.0
            return (positive_score - negative_score) / total
        
        try:
            sentiment = AI_MODELS['sentiment'].polarity_scores(text)
            return sentiment['compound']
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return 0.0
    
    def calculate_relevance_enhanced(self, tech_data: Dict) -> float:
        """Enhanced relevance calculation"""
        if not AI_AVAILABLE:
            return 0.5
        
        try:
            # Get your interests from config
            your_interests = self.config.get('your_interests', {})
            all_interests = []
            for category, interests in your_interests.items():
                all_interests.extend(interests)
            
            if not all_interests:
                return 0.5
            
            tech_text = f"{tech_data['name']} {tech_data.get('description', '')}"
            
            # Calculate similarity with your interests
            max_similarity = 0.0
            for interest in all_interests:
                if 'sentence_transformer' in AI_MODELS:
                    # Use AI embeddings
                    tech_embedding = AI_MODELS['sentence_transformer'].encode([tech_text])
                    interest_embedding = AI_MODELS['sentence_transformer'].encode([interest])
                    if 'sklearn' in AI_MODELS:
                        similarity = cosine_similarity(tech_embedding, interest_embedding)[0][0]
                        max_similarity = max(max_similarity, similarity)
                else:
                    # Use simple similarity
                    similarity = self.simple_similarity(tech_text, interest)
                    max_similarity = max(max_similarity, similarity)
            
            return float(max_similarity)
            
        except Exception as e:
            print(f"Error calculating relevance: {e}")
            return 0.5
    
    def enhance_trend_with_ai(self, trend: Dict) -> Dict:
        """Enhance a single trend with AI analysis"""
        enhanced = trend.copy()
        
        # Add AI categorization
        enhanced['ai_category'] = self.categorize_tech_enhanced(trend)
        
        # Add sentiment analysis
        description = f"{trend.get('name', '')} {trend.get('description', '')}"
        enhanced['sentiment_score'] = self.analyze_sentiment_enhanced(description)
        
        # Add relevance scoring
        enhanced['relevance_score'] = self.calculate_relevance_enhanced(trend)
        
        return enhanced
    
    def generate_enhanced_radar(self, trends: List[Dict]) -> Dict[str, List[str]]:
        """Generate enhanced tech radar"""
        
        # Sort by relevance and sentiment
        trends.sort(key=lambda x: (x.get('relevance_score', 0.5), x.get('sentiment_score', 0)), reverse=True)
        
        # Initialize categories
        categorized = {cat: [] for cat in self.categories}
        
        # Categorize technologies
        for trend in trends:
            category = trend.get('ai_category', 'assess')
            if category in categorized:
                tech_name = trend["name"]
                if trend.get('language'):
                    tech_name = f"**{tech_name}** ({trend['language']})"
                else:
                    tech_name = f"**{tech_name}**"
                
                # Add insights
                relevance = trend.get('relevance_score', 0.5)
                sentiment = trend.get('sentiment_score', 0)
                
                if relevance > 0.7:
                    tech_name += " 🔥"  # High relevance
                if sentiment > 0.3:
                    tech_name += " ⭐"  # Positive sentiment
                
                if tech_name not in [item.split("**")[1] if "**" in item else item for item in categorized[category]]:
                    categorized[category].append(tech_name)
        
        # Add current tech to maintain consistency
        current_tech = {
            "adopt": [
                "**FastAPI**", "**Terraform**", "**AWS Lambda/ECS**",
                "**Amazon Kendra** for enterprise search",
                "**Bedrock** for managed LLM access"
            ],
            "trial": [
                "**LangGraph** for multi-step agents",
                "**LiteLLM** as an LLM router",
                "**Guardrails / JSON schema validation** for LLM outputs"
            ],
            "assess": [
                "**LoRA adapters** for small domain adapts",
                "**Vector DBs**: Weaviate vs. Chroma for small workloads",
                "**RAG triage** (FAQ vs. open-ended vs. CRM)"
            ],
            "avoid": [
                "Direct **DB writes via LLM**",
                "Unbounded **function calling** without budget/guardrails"
            ]
        }
        
        # Merge enhanced insights with current tech
        for category in self.categories:
            current_items = current_tech.get(category, [])
            enhanced_items = categorized[category][:3]
            
            keep_count = max(1, len(current_items) // 2)
            final_items = current_items[:keep_count] + enhanced_items[:2]
            
            categorized[category] = final_items
        
        return categorized
    
    def update_readme_tech_radar(self, tech_radar: Dict[str, List[str]]):
        """Update the tech radar section in README.md"""
        
        if not self.readme_path.exists():
            print("README.md not found!")
            return
        
        # Read current README
        content = self.readme_path.read_text()
        
        # Generate new tech radar content
        new_radar_content = "### Tech Radar 🤖\n"
        new_radar_content += "*AI-enhanced categorization updated every 2 weeks*\n\n"
        
        emojis = {"adopt": "✅", "trial": "🧪", "assess": "👀", "avoid": "⛔"}
        
        for category in self.categories:
            emoji = emojis[category]
            category_title = category.title()
            items = tech_radar.get(category, [])
            
            new_radar_content += f'<details><summary>{emoji} {category_title}</summary>\n\n'
            
            for item in items:
                new_radar_content += f"- {item}\n"
            
            new_radar_content += "</details>\n\n"
        
        # Replace existing tech radar section
        pattern = r"(### Tech Radar.*?\n)(.*?)(### Focus\n)"
        replacement = rf"\1{new_radar_content}\3"
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write updated content
        self.readme_path.write_text(updated_content)
        print("✅ Enhanced tech radar updated successfully!")
    
    def save_enhanced_tech_data(self, trends: List[Dict]):
        """Save enhanced tech trends data"""
        self.tech_data_path.parent.mkdir(exist_ok=True)
        
        data = {
            "last_updated": datetime.now().isoformat(),
            "ai_enhanced": AI_AVAILABLE,
            "ai_models_used": list(AI_MODELS.keys()),
            "total_trends": len(trends),
            "trends": trends,
            "insights": {
                "avg_sentiment": np.mean([t.get('sentiment_score', 0) for t in trends]),
                "avg_relevance": np.mean([t.get('relevance_score', 0.5) for t in trends]),
                "categories_distribution": Counter([t.get('ai_category', 'assess') for t in trends])
            }
        }
        
        self.tech_data_path.write_text(json.dumps(data, indent=2, default=str))
        print(f"📊 Saved {len(trends)} enhanced tech trends")
    
    def should_update_radar(self) -> bool:
        """Check if radar should be updated based on changes"""
        config = self.load_config()
        data_file = self.root / "data" / "tech_trends_ai_fixed.json"
        
        if not data_file.exists():
            print("📊 No previous data found - initial update needed")
            return True
        
        try:
            with open(data_file, 'r') as f:
                old_data = json.load(f)
            
            last_updated = datetime.fromisoformat(old_data.get('last_updated', '2020-01-01'))
            days_since_update = (datetime.now() - last_updated).days
            
            # Check if enough time has passed
            if days_since_update < config.get('update_frequency_days', 1):
                print(f"⏰ Last update was {days_since_update} days ago - skipping")
                return False
            
            # Fetch new data to compare
            new_trends = self.fetch_all_trends()
            old_trends = old_data.get('trends', [])
            
            # Calculate changes
            new_names = {trend['name'] for trend in new_trends}
            old_names = {trend['name'] for trend in old_trends}
            
            new_additions = len(new_names - old_names)
            removed_items = len(old_names - new_names)
            total_changes = new_additions + removed_items
            
            # Check if changes meet threshold
            min_changes = config.get('min_changes_for_update', 3)
            change_percentage = (total_changes / max(len(old_names), 1)) * 100
            threshold = config.get('change_threshold_percentage', 5.0)
            
            print(f"📈 Change analysis:")
            print(f"   - New additions: {new_additions}")
            print(f"   - Removed items: {removed_items}")
            print(f"   - Total changes: {total_changes}")
            print(f"   - Change percentage: {change_percentage:.1f}%")
            print(f"   - Threshold: {threshold}%")
            
            if total_changes >= min_changes or change_percentage >= threshold:
                print(f"✅ Changes detected - update needed")
                return True
            else:
                print(f"⏭️  Insufficient changes - skipping update")
                return False
                
        except Exception as e:
            print(f"⚠️  Error checking for updates: {e}")
            return True  # Update on error to be safe
    
    def run(self):
        """Run the enhanced tech radar update"""
        print("🚀 Starting Smart AI-Enhanced Tech Radar Auto-Update...")
        print(f"🤖 AI Available: {AI_AVAILABLE}")
        print(f"🤖 AI Models: {list(AI_MODELS.keys())}")
        
        # Check if update is needed
        if not self.should_update_radar():
            print("🎯 No meaningful changes detected - radar is up to date!")
            return
        
        # Proceed with update
        trends = self.fetch_all_trends()
        print(f"📈 Found {len(trends)} unique tech trends")
        
        # Process trends with AI enhancement
        enhanced_trends = []
        for trend in trends:
            try:
                enhanced_trend = self.enhance_trend_with_ai(trend)
                enhanced_trends.append(enhanced_trend)
            except Exception as e:
                print(f"⚠️  Error enhancing trend {trend.get('name', 'unknown')}: {e}")
                enhanced_trends.append(trend)
        
        # Generate radar content
        radar_content = self.generate_enhanced_radar(enhanced_trends)
        
        # Update README
        self.update_readme_tech_radar(radar_content)
        
        # Save enhanced data
        self.save_enhanced_tech_data(enhanced_trends)
        
        print("✅ Enhanced tech radar updated successfully!")
        print(f"📊 Saved {len(enhanced_trends)} enhanced tech trends")
        print("🎉 Enhanced tech radar auto-update completed!")

if __name__ == "__main__":
    updater = AITechRadarUpdaterFixed()
    updater.run()
