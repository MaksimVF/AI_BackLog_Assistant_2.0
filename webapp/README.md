


# AI Backlog Assistant Telegram Web App

This is a Telegram Web App (mini-app) that provides a user interface for the AI Backlog Assistant. It allows users to manage tasks, view recommendations, and interact with the system through a web interface embedded in Telegram.

## Features

- Task management (add, view, update)
- Recommendation display
- Status tracking
- Telegram authentication integration
- Responsive design

## How to Use

1. **Deploy the API**: Run the FastAPI backend
2. **Host the Web App**: Serve the HTML file on a web server
3. **Configure Telegram Bot**: Set up the bot to launch the web app

## Files

- `index.html`: Main web app interface
- `api.py`: FastAPI backend for the web app
- `README.md`: This documentation

## Deployment

1. **Run the combined API**:
   ```bash
   uvicorn src.api.main_with_webapp:app --reload
   ```

2. **Host the Web App**:
   - Use any static file server (e.g., nginx, Apache, or a simple Python server)
   - Ensure CORS is configured properly

3. **Configure Telegram Bot**:
   - Use the `web_app` parameter in bot commands to launch the app
   - Example: `await bot.send_message(chat_id, "Open Web App", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open App", web_app={"url": "https://yourdomain.com/webapp"})))`

## Integration with Main System

The web app is now integrated directly into the main AI Backlog Assistant API with the `/webapp` prefix. All routes are served from the same FastAPI instance.

## Development

To run locally:
1. Start the combined API: `uvicorn src.api.main_with_webapp:app --reload`
2. Open the HTML file in a browser
3. For Telegram integration, use tools like ngrok to expose your local server

## Web App API Endpoints

The web app uses the following API endpoints (prefixed with `/webapp`):

- `GET /webapp/tasks` - Get all tasks
- `POST /webapp/tasks` - Create a new task
- `GET /webapp/tasks/{task_id}` - Get a specific task
- `PUT /webapp/tasks/{task_id}` - Update a task
- `GET /webapp/recommendations/{task_id}` - Get recommendations for a task

## Future Enhancements

- Add real-time updates with WebSockets
- Implement more detailed recommendation views
- Add user authentication and authorization
- Integrate with the main recommendation engine


