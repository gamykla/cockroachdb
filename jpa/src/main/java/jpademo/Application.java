package jpademo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class Application {

    private static final Logger log = LoggerFactory.getLogger(Application.class);

    public static void main(String[] args) {
        SpringApplication.run(Application.class);
    }

    @Bean
    public CommandLineRunner demo(AccountRepository repository) {
        return (args) -> {
            // save a couple of customers
            repository.save(new Account("Jack", "Bauer", 1));
            repository.save(new Account("Chloe", "O'Brian", 1));
            repository.save(new Account("Kim", "Bauer", 1));
            repository.save(new Account("David", "Palmer", 1));
            repository.save(new Account("Michelle", "Dessler", 1));

            // fetch all customers
            log.info("Customers found with findAll():");
            log.info("-------------------------------");
            for (Account customer : repository.findAll()) {
                log.info(customer.toString());
            }
            log.info("");

            // fetch an individual customer by ID
            Account customer = repository.findOne(1L);
            log.info("Customer found with findOne(1L):");
            log.info("--------------------------------");
            log.info(customer.toString());
            log.info("");

            // fetch customers by last name
            log.info("Customer found with findByLastName('Bauer'):");
            log.info("--------------------------------------------");
            for (Account bauer : repository.findByLastName("Bauer")) {
                log.info(bauer.toString());
            }
            log.info("");
        };
    }

}
