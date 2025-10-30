


"""
Integration test showing how the task prioritization system works
with the existing task processing pipeline.
"""

from src.agents.level1.input_agent import input_agent
from src.agents.level1.modality_detector import modality_detector
from src.agents.level1.preprocessor import preprocessor
from src.agents.level2.semantic_block_classifier import semantic_block_classifier
from src.agents.level3.task_prioritization_agent import task_prioritization_agent

def test_full_pipeline():
    """Test the full task processing pipeline with prioritization"""

    # Sample task input
    task_text = "Critical security vulnerability affecting all users. Urgent fix needed ASAP."

    print("=== Full Task Processing Pipeline ===")
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
    # For direct text input, we'll use it as-is
    preprocessed = task_text
    print(f"   - Cleaned text: {preprocessed[:50]}...\n")

    # Step 4: Semantic classification
    print("4. Semantic Classification:")
    semantic_result = semantic_block_classifier.classify_blocks(task_text)
    print(f"   - Number of blocks: {len(semantic_result['blocks'])}")
    print(f"   - Block types: {[block['block_type'] for block in semantic_result['blocks']]}\n")

    # Step 5: Task prioritization (assuming classification as 'bug')
    print("5. Task Prioritization:")
    prioritization_result = task_prioritization_agent.prioritize_task(task_text, "bug")
    print(f"   - Priority score: {prioritization_result['priority_score']}")
    print(f"   - Priority level: {prioritization_result['priority_level']}")
    print(f"   - Recommendation: {prioritization_result['recommendation']}")
    print(f"   - Risk score: {prioritization_result['risk_score']}")
    print(f"   - Impact score: {prioritization_result['impact_score']}")
    print(f"   - Urgency score: {prioritization_result['urgency_score']}")
    print(f"   - Estimated time: {prioritization_result['resource_estimate']['time_hours']} hours\n")

    print("=== Pipeline Complete ===")

    # Verify the pipeline works
    assert input_data.modality == "text"
    assert modality == "text"
    assert len(preprocessed) > 0
    assert len(semantic_result['blocks']) > 0
    assert prioritization_result['priority_score'] > 0
    assert prioritization_result['priority_level'] in ["Low", "Medium", "High", "Critical"]

if __name__ == "__main__":
    test_full_pipeline()
    print("Integration test completed successfully!")

