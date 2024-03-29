.PHONY : build
build :
	docker-compose build;

.PHONY : clean
clean :
	docker-compose down;
	docker system prune -a;

.PHONY : all
all :
	docker-compose build;
	docker-compose up;

.PHONY : deamon
deamon :
	docker-compose build;
	docker-compose up --detach;

.PHONY : up
up :
	docker-compose up;
