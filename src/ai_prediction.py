import torch
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class Prediction():
    def __init__(self, token : str = None) -> None:
        if token is None:
            raise ValueError("Hugging Face Token for Gemma 2 is required")
        self.token = token
        self.messages = []
        self.__get_model()

    def __get_model(self):
        # Load the tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            "google/gemma-2-2b-it",
            use_auth_token=self.token  # Automatically uses the token saved during notebook_login
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            "google/gemma-2-2b-it",
            torch_dtype=torch.float32,  # Ensures compatibility with CPU
            use_auth_token=self.token
        )

    def obtain_actions(self, user_inpt):
        instructions = """
        Given user message, detect the intention from the list ["Reply", "Summary"] and generate a natural language response starting with "Reply" or "Summary".
        """

        self.messages.append({"role": "user", "content": f""" {instructions}
            {user_inpt}
        """})

        input_ids = self.tokenizer.apply_chat_template(self.messages[-3:], return_tensors="pt", return_dict=True)

        outputs = self.model.generate(**input_ids, max_new_tokens=512)
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        self.messages.append({"role": "assistant", "content": decoded_output})

    def select_email(self, user_input, email_senders):
        instructions = f"""Select the email the user is referring to. Return its index. Respond in either in a JSON object with a integer "index" or If you are unusable to, then instead return an error message explaining why in the json as a string "error"

        User Response: {user_input}

        User's emails: {email_senders}"""
    
        input_ids = self.tokenizer(instructions, return_tensors="pt")
        outputs = self.model.generate(**input_ids, max_new_tokens=256)
        output_text = self.tokenizer.decode(outputs[0])

        return output_text

    def create_reply(self, user_input, email):
        instructions = f"""
        Given the user query: {user_input}

        Generate an email response to:

        {email}

        Only create the email response. Do not add any explanations.
        """
    
        input_ids = self.tokenizer(instructions, return_tensors="pt")
        outputs = self.model.generate(**input_ids, max_new_tokens=256)
        output_text = self.tokenizer.decode(outputs[0])

        return output_text

    def create_summary(self, user_input, emails, selection_index):
        instructions = f"""
        Given the user query: {user_input}

        Generate an summary of the email "{selection_index}" out of:

        {emails}

        Do not add anything that is not a summary of the email provided.
        """
    
        input_ids = self.tokenizer(instructions, return_tensors="pt")
        outputs = self.model.generate(**input_ids, max_new_tokens=256)
        output_text = self.tokenizer.decode(outputs[0])

        return output_text

    def main(self, user_input, email, selection_index):
        sun_str = str(self.messages[-1]["content"][-15:-1])
        if "Reply" in sun_str:
            reply = self.create_reply(user_input, email)
            return reply

        elif "Summary" in sun_str:
            summary = self.create_summary(user_input, email, selection_index)
            return summary

        else:
            pass
            #pass a message to the bot: respond with Reply or Summary!