package main

import (
	"net/http"

	"github.com/labstack/echo/v4"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"

	"context"
	"fmt"
	"log"
	"time"
)

var client *mongo.Client

func initMongo() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	var err error
	client, err = mongo.Connect(ctx, options.Client().ApplyURI("mongodb://admin:Nox1234@mongodb:27017/"))
	if err != nil {
		log.Fatal("MongoDB connection error", err)
	}

	if err = client.Ping(ctx, readpref.Primary()); err != nil {
		log.Fatal("MongoDB ping error: ", err)
	}

	fmt.Println("MongoDB inits successfully!")
}

func getUsers(c echo.Context) error {
	collection := client.Database("NNS").Collection("events")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	cur, err := collection.Find(ctx, bson.M{})
	if err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{"error": err.Error()})
	}
	defer cur.Close(ctx)

	var results []bson.M
	if err = cur.All(ctx, &results); err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{"error": err.Error()})
	}

	return c.JSON(http.StatusOK, results)
}

func main() {
	initMongo()

	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, 1orld")
	})

	e.GET("/events", getUsers)

	e.Logger.Fatal(e.Start(":3012"))
	print("ekeke")
}
