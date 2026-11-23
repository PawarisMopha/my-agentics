package main

import (
	"context"
	"fmt"
	"log"
        "os"

	"google.golang.org/genai"
	"google.golang.org/genai/interactions/models/interactions"
	"google.golang.org/genai/interactions/models/operations"
        "github.com/lpernett/godotenv"
)

func main() {
	ctx := context.Background()
        err := godotenv.Load()
        if err != nil {
                log.Fatal("Error loading .env file")
        }

        apiKey := os.Getenv("GOOGLE_API_KEY")

	// สร้าง Client แบบระบุ API Key โดยตรง
	client, err := genai.NewClient(ctx, &genai.ClientConfig{
		APIKey:  apiKey,
		Backend: genai.BackendGeminiAPI,
	})
	if err != nil {
		log.Fatal(err)
	}

	// เรียกใช้งาน Interactions API ตามตัวอย่างในรูป
	body := operations.NewCreateInteractionRequestBody(interactions.CreateModelInteraction{
		Model: interactions.Model("gemini-3.8-flash"),
		Input: genai.Ptr(interactions.NewInteractionsInput("Tell me a short joke about programming.")),
	})

	res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{Body: body})
	if err != nil {
		log.Fatal(err)
	}

	if res.Interaction != nil && res.Interaction.GetOutputText() != nil {
                fmt.Println(*res.Interaction.GetOutputText())
        }
}
