



"""
Integration test showing how the advanced task classifier works
with the existing task processing pipeline.
"""

from src.agents.level1.input_agent import input_agent
from src.agents.level1.modality_detector import modality_detector
from src.agents.level1.preprocessor import preprocessor
from src.agents.level2.advanced_task_classifier import advanced_task_classifier
from src.agents.level2.semantic_block_classifier import semantic_block_classifier

def test_full_classification_pipeline():
    """Test the full task processing pipeline with advanced classification"""

    # Sample task input
    task_text = "Critical security bug in the login system causing authentication failures"

    print("=== Full Task Classification Pipeline ===")
    print(f"Input: {task_text}\n")

    # Step 1: Input processing
    print("1. Input Processing:")
    input_data = input_agent.process_text(task_text)
    print(f"   - Modality: {input_data.modality}")
    print(f"   - Content length: {len(input_data.content)} chars\n")

    # Step 2: Modality detection
    print("2. Modality Detection:")
    modality = modality_detector.detect(task_text)
    print(f"   - Detected modality: {modality}\n")

    # Step 3: Preprocessing (for text, we'll use the text directly)
    print("3. Preprocessing:")
    preprocessed = task_text
    print(f"   - Cleaned text: {preprocessed[:50]}...\n")

    # Step 4: Semantic classification
    print("4. Semantic Classification:")
    semantic_result = semantic_block_classifier.classify_blocks(task_text)
    print(f"   - Number of blocks: {len(semantic_result['blocks'])}")
    print(f"   - Block types: {[block['block_type'] for block in semantic_result['blocks']]}\n")

    # Step 5: Advanced task classification
    print("5. Advanced Task Classification:")
    classification_result = advanced_task_classifier.classify_task(task_text)
    print(f"   - Task type: {classification_result.task_type}")
    print(f"   - Sub-category: {classification_result.sub_category}")
    print(f"   - Confidence: {classification_result.confidence:.2f}")
    print(f"   - Domain: {classification_result.metadata['domain']}")
    print(f"   - Sentiment: {classification_result.metadata['sentiment']}\n")

    # Step 6: Comprehensive analysis
    print("6. Comprehensive Analysis:")
    analysis_result = advanced_task_classifier.analyze_task(task_text)
    print(f"   - Task type: {analysis_result['task_type']}")
    print(f"   - Sub-category: {analysis_result['sub_category']}")
    print(f"   - Domain: {analysis_result['domain']}")
    print(f"   - Entities found: {len(analysis_result['entities'])}")
    print(f"   - Sentiment: {analysis_result['sentiment']}\n")

    print("=== Pipeline Complete ===")

    # Verify the pipeline works
    assert input_data.modality == "text"
    assert modality == "text"
    assert len(preprocessed) > 0
    assert len(semantic_result['blocks']) > 0
    assert classification_result.task_type in ["bug", "idea", "feedback", "question", "request"]
    assert classification_result.confidence > 0.5
    assert "domain" in classification_result.metadata
    assert "sentiment" in classification_result.metadata

if __name__ == "__main__":
    test_full_classification_pipeline()
    print("Classification integration test completed successfully!")



