# vonage-real-time-integration-example
Vonage VoiceAPI Real time integration with VoiceAI


# Before you start
- Setup vonage account.
- Create an application with Voice APIs enabled.
- Create private and public key to use with SDK.
- Install ngrok

# Install requirements
```bash
pip install -r requirements.txt
```
# Start a ngrok service
```bash
ngrok http 9999
```

# Start the answer server
In a separate terminal export NGROK_URL and NS_API_KEY and start the uvicorn server.
In order to get NS_API_KEY refer [ here. ](https://voice.neuralspace.ai/docs/get-started#creating-your-api-keys)
```bash
export NGROK_URL=<ngrok public url>
export NS_API_KEY=<APIKEY>
uvicorn answer_server:app --host 0.0.0.0 --port 9999
```

# Make the Vonage call
In a separate terminal run the following command.
```bash
python vonage_make_call.py --answer_url <ngrok url>/answer --application_id <application id> --private_key <local path to private key> --to_number <tonumber> --from_number <from number>

SAMPLE
python vonage_make_call.py --answer_url https://300b-2406-7400-56-cf0d-4125-592-ecad-817f.ngrok.io/answer --application_id 77bf5a13-8f46-48be-9ec5-4d09b8ba380b --private_key private_1.key --to_number 1234567891 --from_number 1234567899
```

# Results
You should be able to see the results in the logs of the server.  
And for reference the recorded audio file of the conversation is saved by the server as `tempfile.wav`