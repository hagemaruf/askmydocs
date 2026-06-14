FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build

WORKDIR /app

COPY . .

RUN dotnet restore AskMyDocs.web.csproj

RUN dotnet publish AskMyDocs.web.csproj -c Release -o /publish

FROM nginx:alpine

COPY --from=build /publish/wwwroot /usr/share/nginx/html

EXPOSE 80