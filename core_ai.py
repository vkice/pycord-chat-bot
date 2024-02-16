import os, openai, time
from datetime import datetime
from collections import deque

# The work flow here is init -> message_respond -> chat -> sys_msg_ret -> openai_prompt, manual modifications can be added at any step
class Chat_Bot():
    
    convo_limit = 8 # Adjust as necessary but this is a good starter number
    
    def __init__(self, environment, conversation_limit: int = convo_limit):
        
        self.client         = openai.OpenAI(api_key=os.environ['OPENAI_KEY'])
        self.chatgpt_model  = 'gpt-4-turbo-preview' # Currently using the GPT4 Turbo preview, but can utilize other, cheaper one like 3.5 Turbo
        self.environment    = environment # Have multiple servers? Separate prompts/sys messages for each one with a special env
        self.extra_msg      = str(' Answer questions in the first person perspective. Do your absolute best to be creative, talk naturally, and conversational. '
            # Enter in any other info here, how you would like it to respond to messages
        )
        self.messages_queue = deque(maxlen=conversation_limit)
        
    
    def chat(self, prompt):
        """Based on context, returns the relative system messages and parameters for the chat response, then calls the OpenAI API"""
        
        sys_msg = self.sys_msg_ret()
        response = self.openai_prompt(sys_msg, prompt)
        # Feel free to add anything else before returning the response here
        return response
        
        
    def sys_msg_ret(self):
        """Returns an accurate current date through a function call"""
        
        if self.environment == "my_server":
            sys_msg = str(f'Today is {datetime.now(): %A %d %B %Y %H:%M} '
                    # Enter in any other info here, such as the identity of the chat bot or where it is located
                )
        else:
            sys_msg = str(f'Today is {datetime.now(): %A %d %B %Y %H:%M}')
            
        return sys_msg
    
    
    def openai_prompt(self, sys_msg, prompt):
        """Send prompt to OpenAI API and returns the response"""
        
        temp              = 1
        max_chars         = 4000 # Setting a character limit for the queue, if over append a blank set
        max_token_ceiling = 3500 # Setting a character limit for GP4 , this way we won't rate limit as easily
        
        
        while len(str(self.messages_queue)) > max_chars:
            self.messages_queue.append({"role": "user", "content": " "})
        max_tokens_len = (max_token_ceiling - len(sys_msg) - len(self.extra_msg) - len(str(self.messages_queue)))
        
        sleep_time = 35 # API rate limiting measure, simple sleep and wait if messages are rapidly sent to the chat bot
        for i in range(0,10):

            try:
                
                if max_tokens_len < 100:
                    max_tokens_len = 500 # In case we underflow the max tokens
                chat_compl = self.client.chat.completions.create(
                    model = self.chatgpt_model, 
                    messages = [
                        {"role": "system", "content": sys_msg}, 
                        *self.messages_queue, 
                        {"role": "user", "content": self.extra_msg}, 
                        {"role": "user", "content": prompt}
                    ], 
                    temperature = temp, 
                    max_tokens = max_tokens_len
                )
                response = str(chat_compl.choices[0].message.content)
                self.messages_queue.append({"role": "user", "content": prompt})
                self.messages_queue.append({"role": "assistant", "content": response})
                return response
            
            except Exception as e:
                
                print(f"OpenAI API Error, retrying in {sleep_time} seconds: {e}")
                time.sleep(sleep_time)
                sleep_time += 15
                continue


    async def message_respond(self, prompt, discord_message, msg_ctx):
        """Responds to the message"""

        response = self.chat(prompt=prompt)
        
        if len(response) > 1950: # Discord has a character limit of 2000, breaking up response as multiple messages
            long_resp = []
            while len(response) > 1950:
                long_resp.append(response[0:1950])
                response = response[1950:]
            long_resp.append(response)
            is_long_response = True
        else:
            is_long_response = False
            
        try:
            if msg_ctx == None : # Channel monitoring
                if is_long_response:
                    await discord_message.reply(long_resp[0])
                    for msg in long_resp[1:]:
                        await discord_message.send(msg)
                else:
                    await discord_message.reply(response)
                    
            else: # Slash command
                if is_long_response:
                    await msg_ctx.respond(long_resp[0])
                    for msg in long_resp[1:]:
                        await msg_ctx.send(msg)
                else:
                    await msg_ctx.respond(response)
                
        except Exception as e:
                
            print(f"Error occurred responding to message: {e}")
        
        return
    