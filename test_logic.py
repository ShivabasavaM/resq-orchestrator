from app.graph.workflow import app_graph

# Simulate a user message
inputs = {
    "user_input": "There is a massive fire at the industrial estate in Hyderabad! We need fire trucks and burn specialists immediately.",
    "messages": []
}

print("Running simulation...")
# Stream the output to see steps happen in real-time
for output in app_graph.stream(inputs):
    for key, value in output.items():
        print(f"Finished Node: {key}")
        print("Updated State:", value)