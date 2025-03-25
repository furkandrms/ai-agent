from tasks.base_task import BaseTask
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.twitter_api import post_tweet


class TweetTask(BaseTask):

    def execute(self, personality):
        
        prompt_template = PromptTemplate.from_template(
            "Write a {style}, {tone} tweet about {topic}. Keep it under 280 characters. Be authentic and engaging."
            )
        
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        chain = LLMChain(llm=llm, prompt=prompt_template)

        tweet = chain.run({

            "style": personality["style"],
            "tone": personality["tone"],
            "topic": personality["topic"]
        })

        print(f"[TWEET] Generated Tweet: \n{tweet}\n")
        post_tweet(tweet)
        print("[TWEET] Tweet posted successfully.")