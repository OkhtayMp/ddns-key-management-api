# Dynamic DNS (DDNS) Key Management API

This is a Flask-based API designed for managing Dynamic DNS (DDNS) keys and associating them with IP addresses. The API allows users to generate, list, remove keys, and update IP addresses associated with each key. This is useful for dynamic IP management, where keys can be associated with changing IPs.

## Features

- **Create a new DDNS key**
- **List all keys and their associated IPs**
- **Remove a DDNS key**
- **Add an IP address to a key**
- **Retrieve the IP address associated with a key**

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/okhtaymp/ddns-key-management-api.git
    cd ddns-key-management-api
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python main.py
    ```

   By default, the app will run on `http://127.0.0.1:5000`.

## How to generate and use your own admin key

You can generate your own admin key using the `uuidgen` command and then set it in the `ADMIN_KEY` environment variable. This key is used to access all the endpoints that require admin permissions (e.g., `/create_key`, `/list_key`, `/remove_key`).

### Step 1: Generate an Admin Key

To generate a new UUID (which will serve as your admin key), run the following command:

```bash
uuidgen
```

This will output something like: 

```bash
35c1dbca-c958-4dad-9f7d-a9fba8aa79e5
```

### Step 2: Set the Admin Key in the Environment Variable

Once you have your UUID, you can set it as the `ADMIN_KEY` environment variable. You can do this by running the following command in your terminal:

```bash
export ADMIN_KEY="35c1dbca-c958-4dad-9f7d-a9fba8aa79e5"
```

Alternatively, you can set this variable permanently by adding it to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
echo 'export ADMIN_KEY="35c1dbca-c958-4dad-9f7d-a9fba8aa79e5"' >> ~/.bashrc
source ~/.bashrc
```

Now, the `ADMIN_KEY` environment variable will be available for all terminal sessions.

### Step 3: Use the Admin Key in API Requests

After setting your admin key, you can use it in your API requests. Here are some examples:

#### 1. **Create a new DDNS key**

- **URL:** `/create_key/<admin_key>`
- **Method:** `GET`
- **Example `curl`:**

```bash
curl "http://127.0.0.1:5000/create_key/$ADMIN_KEY"
```

#### 2. **List all DDNS keys**

- **URL:** `/list_key/<admin_key>`
- **Method:** `GET`
- **Example `curl`:**

```bash
curl "http://127.0.0.1:5000/list_key/$ADMIN_KEY"
```

#### 3. **Remove a DDNS key**

- **URL:** `/remove_key/<admin_key>`
- **Method:** `POST`
- **Example `curl`:**

```bash
curl -X POST "http://127.0.0.1:5000/remove_key/$ADMIN_KEY" -H "Content-Type: application/json" -d '{"key": "********-****-****-****-************"}'
```

#### 4. **Add an IP address to a key**

- **URL:** `/add_ip/<key>`
- **Method:** `POST`
- **Example `curl`:**

```bash
curl -X POST "http://127.0.0.1:5000/add_ip/$KEY" -H "Content-Type: application/json" -d '{"ip": "192.168.1.100"}'
```

#### 5. **Get the IP address associated with a key**

- **URL:** `/get_ip/<key>`
- **Method:** `GET`
- **Example `curl`:**

```bash
curl "http://127.0.0.1:5000/get_ip/$KEY"
```

## API Endpoints

### 1. **Create a new DDNS key**

- **URL:** `/create_key/<admin_key>`
- **Method:** `GET`
- **Description:** Generates a new DDNS key and adds it to the system.
- **Admin Key:** You must provide the correct admin key as part of the URL.

#### Example `curl`:

```bash
curl "http://127.0.0.1:5000/create_key/$ADMIN_KEY"
```

- **Response:** A new DDNS key will be returned in JSON format.

```json
{
    "key": "new-generated-uuid"
}
```

### 2. **List all DDNS keys**

- **URL:** `/list_key/<admin_key>`
- **Method:** `GET`
- **Description:** Lists all the keys and their associated IP addresses.
- **Admin Key:** You must provide the correct admin key as part of the URL.

#### Example `curl`:

```bash
curl "http://127.0.0.1:5000/list_key/$ADMIN_KEY"
```

- **Response:** A list of DDNS keys with their associated IPs.

```json
[
    {
        "key": "********-****-****-****-************",
        "ip": "192.168.1.1"
    },
    {
        "key": "********-****-****-****-************",
        "ip": "192.168.1.2"
    }
]
```

### 3. **Remove a DDNS key**

- **URL:** `/remove_key/<admin_key>`
- **Method:** `POST`
- **Description:** Removes the specified DDNS key from the system.
- **Admin Key:** You must provide the correct admin key as part of the URL.
- **Request Body:** A JSON object with the `key` to remove.

#### Example `curl`:

```bash
curl -X POST "http://127.0.0.1:5000/remove_key/$ADMIN_KEY" -H "Content-Type: application/json" -d '{"key": "********-****-****-****-************"}'
```

- **Response:** A message confirming the removal of the key.

```json
{
    "message": "Key ********-****-****-****-************ removed"
}
```

### 4. **Add an IP address to a key**

- **URL:** `/add_ip/<key>`
- **Method:** `POST`
- **Description:** Adds an IP address to the specified DDNS key.
- **Request Body:** A JSON object with the `ip` to associate with the key.

#### Example `curl`:

```bash
curl -X POST "http://127.0.0.1:5000/add_ip/********-****-****-****-************" -H "Content-Type: application/json" -d '{"ip": "192.168.1.100"}'
```

- **Response:** The key and the associated IP.

```json
{
    "key": "********-****-****-****-************",
    "ip": "192.168.1.100"
}
```

### 5. **Get the IP address associated with a key**

- **URL:** `/get_ip/<key>`
- **Method:** `GET`
- **Description:** Retrieves the IP address associated with the specified DDNS key.

#### Example `curl`:

```bash
curl "http://127.0.0.1:5000/get_ip/********-****-****-****-************"
```

- **Response:** The key and its associated IP.

```json
{
    "key": "********-****-****-****-************",
    "ip": "192.168.1.100"
}
```

Alternatively, to check for the IP directly and avoid `null` values, you can use:

```bash
curl -s http://127.0.0.1:5000/get_ip/2a66f686-d04c-4843-b1cc-6f5a2d030f42 | jq -r '.ip // "No IP found"'
```

This will return the IP if found, or `"No IP found"` if the key does not have an associated IP.

#### Response:

```bash
192.168.1.100
```

## Authentication

To access the endpoints that require an admin key (`/create_key`, `/list_key`, `/remove_key`), you need to pass the correct admin key in the URL. The default admin key is: `35c1dbca-c958-4dad-9f7d-a9fba8aa79e5`