# postgresql call import
#============================================================================#
from functions.postgresql_function import save_data , get_user_messages

# realestate  call import
#============================================================================#
from functions.RealEstate_Recommendation import RealEstateRecommendationTool

# LangChain function call 
#============================================================================#
# Import things that are needed generically
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

from datetime import datetime
# Api key setting
#============================================================================#
from dotenv import load_dotenv


load_dotenv()


def Agent_Run(question):
    # Set Memory
    #============================================================================#
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

    chat_history = get_user_messages('U50103dd3166e13e2ffa18b6b2266c77f')
    if chat_history != None :
        for row_data in chat_history :
            memory.save_context({"input": row_data[0]}, {"output": row_data[1]})
    else:
        print("Data Read Not Work")
    #============================================================================#
    
    model = ChatOpenAI( 
                    model="gpt-4-1106-preview" ,
                    temperature= 0.9
                )
    tools = [RealEstateRecommendationTool()]
    agent = initialize_agent(tools, 
                    model, 
                    agent= AgentType.OPENAI_FUNCTIONS, 
                    verbose= True,
                    memory = memory,
                    agent_kwargs = agent_kwargs
    )
    agent_ans = agent.run(question)

    try:
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))

        user = {
                "user_id" : "U50103dd3166e13e2ffa18b6b2266c77f" , 
                "user_message": question , 
                "timestamp" :  timestamp
        }
        agent = {
                "agent_message" : agent_ans 
        }
        save_data(user = user , agent = agent)
    
    except:
        pass 

    return agent_ans 

while(True):
    question = input("please enter question: ")

    if question == "Q":
        break

    ans = Agent_Run(question)
    print(ans)