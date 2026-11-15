# Production image: build the Jekyll site, then serve the static output with nginx.
# Dokploy builds this on every deploy (see .github/workflows/ci.yml).

FROM ruby:3.3 AS build
WORKDIR /srv/site
ENV JEKYLL_ENV=production

# Gems first so this layer is cached until the Gemfile changes.
COPY Gemfile ./
RUN bundle install --jobs 4

COPY . .
RUN bundle exec jekyll build -d /srv/_site

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /srv/_site /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO /dev/null http://127.0.0.1/ || exit 1
