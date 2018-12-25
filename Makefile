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