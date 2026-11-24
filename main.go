package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/lpernett/godotenv"
	"google.golang.org/genai"
	"google.golang.org/genai/interactions/models/interactions"
	"google.golang.org/genai/interactions/models/operations"
)

func main() {
	// 1. โหลดค่าจากไฟล์ .env
	err := godotenv.Load()
	if err != nil {
		log.Println("ไม่พบไฟล์ .env จะใช้ค่าจาก System Environment แทน")
	}

	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		apiKey = os.Getenv("GOOGLE_API_KEY")
	}
	if apiKey == "" {
		log.Fatal("ไม่พบค่า GEMINI_API_KEY หรือ GOOGLE_API_KEY")
	}

	// 2. ตั้งค่า Timeout และสร้าง Client
	ctx, cancel := context.WithTimeout(context.Background(), 90*time.Second)
	defer cancel()

	client, err := genai.NewClient(ctx, &genai.ClientConfig{
		APIKey:  apiKey,
		Backend: genai.BackendGeminiAPI,
	})
	if err != nil {
		log.Fatal(err)
	}

	// 3. กำหนดหัวข้อที่ต้องการให้ Agent ค้นหาเว็บและสรุปผล
	prompt := "ค้นหาข่าวอัปเดตล่าสุดเกี่ยวกับ Go programming language และ Open Source AI Tools ในสัปดาห์นี้ แล้วสรุปเป็นข้อๆ"

	// 4. สร้าง Request โดยเปิดใช้งาน Tool Google Search
	body := operations.NewCreateInteractionRequestBody(interactions.CreateModelInteraction{
		Model: interactions.Model("gemini-3.6-flash"),
		Input: genai.Ptr(interactions.NewInteractionsInput(prompt)),
		Tools: []interactions.Tool{
			{
				GoogleSearch: &interactions.GoogleSearch{},
			},
		},
	})

	res, err := client.Interactions.Create(ctx, operations.CreateInteractionRequest{
		Body: body,
	})
	if err != nil {
		log.Fatal(err)
	}

	// 5. แสดงผลลัพธ์ข้อความจาก OutputText
	if res.Interaction != nil && res.Interaction.GetOutputText() != nil {
		fmt.Println(*res.Interaction.GetOutputText())
	}
}

