# blog-site

Personal blog built with Jekyll and the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme.

## Run locally

```bash
docker compose up        # http://localhost:4000, live reload
```

With Ruby 3.1+ installed you can run `bundle install && bundle exec jekyll serve` instead.

## Where things live

| Path | What |
| --- | --- |
| `_posts/` | Posts, named `YYYY-MM-DD-slug.md`; the URL is `/slug/` |
| `_projects/` | One file per project; listed by `_layouts/projects.html` at `/projects/` |
| `_tabs/` | Sidebar pages (projects, categories, tags, archives, about) |
| `_data/contact.yml` | Sidebar contact icons |
| `images/` | Post and project images |
| `_config.yml` | Title, tagline, avatar, social links, site `url` |

A post's `image.path` is the preview on the home page and the banner on the post.

## Deployment

Live at <https://blog.ruudjuffermans.nl>, hosted on Dokploy.

- `Dockerfile` builds the site with Jekyll and serves `_site` with nginx (`nginx.conf`) on port 80.
- `.github/workflows/ci.yml` builds the site, runs html-proofer and builds the image on every push.
  On `main`, once those pass, it calls the Dokploy deploy webhook, which pulls `main` and rebuilds.
- The webhook URL is the repository secret `DOKPLOY_WEBHOOK_URL`
  (Dokploy → the application → Deployments → Webhook URL).

Try the production image locally: `docker build -t blog-site . && docker run --rm -p 8080:80 blog-site`.
