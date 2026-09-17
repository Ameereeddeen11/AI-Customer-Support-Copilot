"""
This module implements an agent that interacts with a customer support system for an e-shop.
The agent uses the Ollama API to process user queries, determine if they relate to order status,
and call the appropriate tools to retrieve information.
"""

import json
import ollama

from src.rag_query import OLLAMA_HOST
from src.tools import Tools, Available_Tools

ollama_client = ollama.Client(host=OLLAMA_HOST)

system_prompt = """
    Jsi zákaznická podpora e-shopu. Máš k dispozici nástroj
    na zjištění stavu objednávky. Pokud se zákazník ptá na objednávku a
    zmíní její ID, VŽDY nejdřív zavolej nástroj zjisti_stav_objednavky -
    nikdy si stav objednávky nevymýšlej. Pokud zákazník ID objednávky
    neuvede, zdvořile se ho zeptej na ID
"""

def run_agent (
    user_query: str,
    model_llm: str = "qwen2.5:14b"
) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    response = ollama_client.chat(
        model=model_llm,
        messages=messages,
        tools=Tools,
        options={"temperature": 0.1}
    )

    model_response = response["message"]

    tool_calls = model_response.get("tool_calls")

    if not tool_calls:
        return model_response["content"]

    messages.append(model_response)

    for calling in tool_calls:
        tool_name = calling["function"]["name"]
        parameters = calling["function"]["arguments"]

        print(f"Agent calling tool: {tool_name} with parameters: {parameters}")

        function = Available_Tools.get(tool_name)

        if function is None:
            result = {
                "error": f"Tool '{tool_name}' not found."
            }
        else:
            result = function(**parameters)

        messages.append({
            "role": "tool",
            "content": json.dumps(result, ensure_ascii=False)
        })

    final_response = ollama_client.chat(
        model=model_llm,
        messages=messages,
        options={"temperature": 0.1}
    )

    return final_response["message"]["content"]

if __name__ == "__main__":
    # test_queries = [
    #     "Jaký je stav mé objednávky ORD-1002?",
    #     "Kdy dorazí objednávka ORD-1999?",
    #     "Jaké máte otevírací hodiny?",
    # ]

    test_queries = [
        "Jaký je stav mé objednávky OBJ-1002?",
        "Kdy dorazí objednávka OBJ-9999?",  # neexistující ID
        "Jaké máte otevírací hodiny?",  # nesouvisí s objednávkami vůbec
    ]

    for query in test_queries:
        print(f"\nUser Query: {query}\n")
        print(run_agent(query))
        print("\n" + "=" * 60)