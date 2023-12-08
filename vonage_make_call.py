import vonage
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--answer_url", type=str, required=True)
    parser.add_argument("--application_id", type=str, required=True)
    parser.add_argument("--private_key", type=str, required=True, help="path to private key")
    parser.add_argument("--to_number", type=str, required=True, help="phone number with country code without +")
    parser.add_argument("--from_number", type=str, required=True, help="phone number with country code without + and should be bought for the vonage application for Voice APIs.")
    args = parser.parse_args()

    answer_url = args.answer_url
    application_id = args.application_id
    private_key = args.private_key
    to_number = args.to_number
    from_number = args.from_number

    client = vonage.Client(
        application_id=application_id, private_key=private_key
    )
    client.voice.create_call(
        {
            "to": [{"type": "phone", "number": to_number}],
            "from": {"type": "phone", "number": from_number},
            "answer_url": [answer_url],
        }
    )


if __name__ == "__main__":
    main()