# test
## Environment Variables

* `DATABASE_URL`:
    * The connection string for your PostgreSQL database.
    * Example: `postgresql://user:password@host:port/database`
    * Required for database access.

* `API_KEY`:
    * An API key for external services.
    * Example: `your_api_key_123`
    * Required if using external APIs.

## Deployment

### Heroku

To deploy to Heroku, set the environment variables using the Heroku CLI:

```bash
heroku config:set DATABASE_URL="your_production_database_url"
heroku config:set API_KEY="your_production_api_key"
