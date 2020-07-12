clean:
	find . -name '*.pyc' -delete
	docker system prune

test:
	docker-compose up -d postgres
	sleep 5
	docker-compose up hasker-tests
	docker-compose down

run:
	docker-compose up -d

stop:
	docker-compose down

prod:
	docker-compose up -d postgres
	sleep 5
	docker-compose up -d hasker
