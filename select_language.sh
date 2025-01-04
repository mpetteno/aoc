#!/bin/bash

# Load the environment variable from the .env file
source .env

# List of programming languages
languages=(
  "Python"
  "JavaScript"
  "TypeScript"
  "Java"
  "Rust"
  "C++"
  "Scala"
  "Kotlin"
  "Perl"
  "Lua"
  "Ruby"
  "Golang"
  "Swift"
  "ObjectiveC"
)

# Last used language (from the env file)
last_used_language=${LAST_USED_LANGUAGE}

# Function to select a random language different from the last used one
select_random_language() {
    # Get a list of languages excluding the last used one
    available_languages=()
    for language in "${languages[@]}"; do
        if [[ "$language" != "$last_used_language" ]]; then
            available_languages+=("$language")
        fi
    done
    # Select a random language from the remaining options
    random_language=${available_languages[$RANDOM % ${#available_languages[@]}]}
    echo "Selected language: $random_language"
    # Update the .env file with the new selected language
    update_env_file "$random_language"
}

# Function to update the .env file with the new value
update_env_file() {
    new_language=$1
    # Update the LAST_USED_LANGUAGE in the .env file
    if grep -q "LAST_USED_LANGUAGE" .env; then
        # If the variable exists, update it
        sed -i '' "s/^LAST_USED_LANGUAGE=.*/LAST_USED_LANGUAGE=$new_language/" .env
    else
        # If the variable doesn't exist, append it
        echo "LAST_USED_LANGUAGE=$new_language" >> .env
    fi
}

# Run the function
select_random_language