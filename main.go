package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

        "google.golang.org/genai"
	"google.golang.org/genai"
	"google.golang.org/genai/interactions"
	"google.golang.org/genai/operations"
	"google.golang.org/genai/interactions/models/interactions"
	"google.golang.org/genai/interactions/models/operations"
	"github.com/lpernett/godotenv"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 90*time.Second)
	defer cancel()

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

	client, err := genai.NewClient(ctx, &genai.ClientConfig{
		APIKey:  apiKey,
		Backend: genai.BackendGeminiAPI,
	})
	if err != nil {
		log.Fatal(err)
	}

	// กำหนดหัวข้อที่ต้องการให้ Agent ค้นหาเว็บและสรุปผล
	prompt := "ค้นหาข่าวอัปเดตล่าสุดเกี่ยวกับ Go programming language และ Open Source AI Tools ในสัปดาห์นี้ แล้วสรุปเป็นภาษาไทยแบบอ่านง่าย แบ่งเป็นหัวข้อ พร้อมแนบลิงก์อ้างอิง"

	res, err := client.Interactions.Create(ctx, &interactions.CreateModelInteractionParams{
		Model: interactions.Model("gemini-3.6-flash"),
		Input: interactions.NewInput(prompt),
		Tools: []interactions.ToolUnion{
			interactions.NewGoogleSearchTool(),
		},
	})
	if err != nil {
		log.Fatalf("เกิดข้อผิดพลาดในการเรียก Gemini API: %v", err)
	}

	outputText := ""
	if res.Interaction != nil && res.Interaction.GetOutputText() != nil {
		outputText = *res.Interaction.GetOutputText()
	}

	if err := os.MkdirAll("output", 0755); err != nil {
		log.Fatal(err)
	}

	filename := filepath.Join("output", fmt.Sprintf("summary-%s.md", time.Now().Format("2006-01-02")))
	content := fmt.Sprintf("# รายงานสรุปข้อมูลประจำวันที่ %s\n\n%s\n", time.Now().Format("2006-01-02"), outputText)

	if err := os.WriteFile(filename, []byte(content), 0644); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("สร้างไฟล์สรุปเรียบร้อยแล้ว: %s\n", filename)
}
