# StayEase API Documentation

## 1. Send Message
**Endpoint:** `POST /api/chat/{conversation_id}/message`


### Request Schema
| Field     | Type     | Description                   |
| :-------- | :------- | :---------------------------- |
| `message` | `string` | The text input from the user. |

### Response Schema
| Field       | Type      | Description                                       |
| :---------- | :-------- | :------------------------------------------------ |
| `messages`  | `array`   | List of role/content objects from the assistant.  |
| `escalated` | `boolean` | Flag indicating if a human agent is now required. |

**Request Body Example:**
```json
{
  "message": "I need a room in Cox's Bazar for 2 nights for 2 guests"
}
```

**Successful Response (200 OK):**
```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "I found several options in Cox's Bazar! The most popular is 'Ocean View Resort' for 5,500 BDT per night. Would you like to see more details or explore other options?"
    }
  ],
  "escalated": false
}
```

## Realistic Example with multi-turn Conversation:

`Turn 1: User asks for hotels`
```json
{
  "message": "I need a room in Cox's Bazar for 2 nights for 2 guests"
}
```
`Turn 2: Agent asks for check-in date`
```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "Sure! To find the best options for you, could you let me know the check-in date you’re planning to arrive? Once I have that, I’ll search for available rooms in Cox’s Bazar for 2 nights for 2 guests."
    }
  ],
  "escalated": false
}
```

`Turn 3: User gives wrong check-in date`

```json
{
  "message": "I am planning to check-in on 28.04.31"
}
```

`Turn 4: LLM again asks for correct date with proper format`

```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "It looks like the date you entered isn’t in a valid format. Could you please provide the check-in date in **YYYY-MM-DD** format (for example, 2026-04-28)? Once I have the correct date, I’ll search for available rooms in Cox’s Bazar for 2 nights for 2 guests."
    }
  ],
  "escalated": false
}
```

`Turn 5: User gives correct date`

```json
{
  "message": "I am planning to check-in on 2026.04.29"
}
```

`Turn 6: Agent gives hotels list with details`

```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "Here are the available rooms in Cox’s Bazar for a 2-night stay (29 Apr – 01 May 2026) for 2 guests:\n\n| # | Property | Rate (BDT/night) | Total (2 nights) | Listing ID |\n|---|---|---|---|---|\n| 1 | Ocean View Resort | 5,500 | 11,000 | 1 |\n| 2 | Beachside Haven | 4,200 | 8,400 | 2 |\n| 3 | Royal Tulip Sea Pearl | 8,500 | 17,000 | 5 |\n| 4 | Long Beach Hotel | 6,800 | 13,600 | 10 |\n| 5 | Hotel Sea Crown | 3,900 | 7,800 | 14 |\n\n**Next steps**\n1. **Choose a property** – let me know the listing ID (1, 2, 5, 10, or 14) you’d like to book.\n2. **Provide your full name** – this will be used for the reservation."
    }
  ],
  "escalated": false
}
```
`Turn 7:User give hotel id for booking`

```json
{
  "message": "I want to book listing id 1. Name: Imtiaz"
}
```
`Turn 8: Agent books hotel and returns booking id`


```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "🎉 **Booking Confirmed!**\n\n- **Guest:** Imtiaz\n- **Property:** Ocean View Resort (Listing ID 1)\n- **Check-in:** 29 Apr 2026\n- **Nights:** 2\n- **Total Price:** 11,000 BDT\n- **Booking ID:** 565dca59-15c7-4293-9fd0-60b7a5e1321d\n\nYou’ll receive a confirmation email shortly with all the details. If you need anything else—extra amenities, transportation, or local tips—just let me know! Safe travels!"
    }
  ],
  "escalated": false
}
```

## Error Response

### 400 Bad Request (Invalid Message Format)
This occurs if the user sends an empty string or the JSON body is malformed.
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error (Backend Failure)
This occurs if the LLM provider (Groq) or the Database (Neon) is unreachable.
```json
{
  "detail": "Internal Server Error. Please check server logs."
}
```

### 422 Unprocessable Entity (Validation Error)
This occurs if the LLM provides invalid arguments to a tool (e.g., wrong date format).
```json
{
  "detail": [
    {
      "loc": ["body", "check_in_date"],
      "msg": "invalid date format",
      "type": "value_error.date"
    }
  ]
}
```


## 2. Get Conversation History
**Endpoint:** `GET /api/chat/{conversation_id}/history`

**Description:** Retrieve the full message history for a specific conversation.

### Response Schema
| Field             | Type     | Description                                                       |
| :---------------- | :------- | :---------------------------------------------------------------- |
| `conversation_id` | `string` | The unique session identifier.                                    |
| `history`         | `array`  | List of objects containing `role` (user/assistant) and `content`. |

**Successful Response (200 OK):**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "history": [
    {
      "role": "user",
      "content": "I need a room in Cox's Bazar"
    },
    {
      "role": "assistant",
      "content": "How many guests and for how many nights?"
    },
  ]
}
```


## Realistic Example
```json
{
  "conversation_id": "1000",
  "history": [
    {
      "role": "user",
      "content": "I need a room in Cox's Bazar for 2 nights for 2 guests"
    },
    {
      "role": "assistant",
      "content": "Sure! To find the best options for you, could you let me know the check‑in date you’re planning to arrive? Once I have that, I’ll search for available rooms in Cox’s Bazar for 2 nights for 2 guests."
    },
    {
      "role": "user",
      "content": "I am planning to check-in on 28.04.31"
    },
    {
      "role": "assistant",
      "content": "It looks like the date you entered isn’t in a valid format. Could you please provide the check‑in date in **YYYY‑MM‑DD** format (for example, 2026‑04‑28)? Once I have the correct date, I’ll search for available rooms in Cox’s Bazar for 2 nights for 2 guests."
    },
    {
      "role": "user",
      "content": "I am planning to check-in on 2026.04.29"
    },
    {
      "role": "assistant",
      "content": "Found 5 properties in Cox's Bazar:\n- Ocean View Resort: 5500 BDT/night (ID: 1)\n- Beachside Haven: 4200 BDT/night (ID: 2)\n- Royal Tulip Sea Pearl: 8500 BDT/night (ID: 5)\n- Long Beach Hotel: 6800 BDT/night (ID: 10)\n- Hotel Sea Crown: 3900 BDT/night (ID: 14)\n"
    },
    {
      "role": "assistant",
      "content": "Here are the available rooms in Cox’s Bazar for a 2‑night stay (28 Apr – 30 Apr 2026) for 2 guests:\n\n| # | Property | Rate (BDT/night) | Total (2 nights) | Listing ID |\n|---|----------|------------------|------------------|------------|\n| 1 | Ocean View Resort | 5,500 | 11,000 | 1 |\n| 2 | Beachside Haven | 4,200 | 8,400 | 2 |\n| 3 | Royal Tulip Sea Pearl | 8,500 | 17,000 | 5 |\n| 4 | Long Beach Hotel | 6,800 | 13,600 | 10 |\n| 5 | Hotel Sea Crown | 3,900 | 7,800 | 14 |\n\n**Next steps**\n\n1. **Choose a property** – let me know the listing ID (1, 2, 5, 10, or 14) you’d like to book.  \n2. **Provide your full name** – this will be used for the reservation.  \n\nOnce I have those details, I’ll create the booking for you."
    },
    {
      "role": "user",
      "content": "I want to book listing id 1. Name: Imtiaz"
    },
    {
      "role": "assistant",
      "content": "SUCCESS: Booking confirmed for Imtiaz at Ocean View Resort!\n- Booking ID: 565dca59-15c7-4293-9fd0-60b7a5e1321d\n- Check-in: 2026-04-29\n- Nights: 2\n- Total Price: 11000 BDT"
    },
    {
      "role": "assistant",
      "content": "🎉 **Booking Confirmed!**\n\n- **Guest:** Imtiaz  \n- **Property:** Ocean View Resort (Listing ID 1)  \n- **Check‑in:** 29 Apr 2026  \n- **Nights:** 2  \n- **Total Price:** 11,000 BDT  \n- **Booking ID:** 565dca59-15c7-4293-9fd0-60b7a5e1321d  \n\nYou’ll receive a confirmation email shortly with all the details and a QR code for check‑in. If you need anything else—extra amenities, transportation, or local tips—just let me know! Safe travels!"
    },
  ]
}
```


---

## Error Responses

### 404 Not Found
Returned if the `conversation_id` does not exist.
```json
{
  "detail": "Conversation history not found."
}
```

### 400 Bad Request
Returned for invalid request bodies or parameters.
```json
{
  "detail": "Invalid message format."
}
```
