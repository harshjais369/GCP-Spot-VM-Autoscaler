import google.cloud.compute_v1 as compute_v1
import time

# TODO: Set these values before running the script.
PROJECT_ID = '' # ie. 'project_name'
INSTANCES = [] # ie. [['instance', 'zone'], ...]
RETRY_LIMIT = 3

def wait_for_operation(operation, verbose_name="operation", timeout=300):
    """
    Waits for the specified operation to complete.

    If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def main():
    delay = 20
    restart_i = 1
    err_i = 0

    instance_client = compute_v1.InstancesClient()

    while True:
        if err_i >= RETRY_LIMIT:
            print('Maximum error limit reached!\nPlease have a look over the hood...')
            break
        for INSTANCE in INSTANCES:
            instance = instance_client.get(project=PROJECT_ID, zone=INSTANCE[1], instance=INSTANCE[0])
            print(f'STATE: {instance.name} - {instance.status}')
            if instance.status == 'TERMINATED':
                # Restart the instance
                try:
                    operation = instance_client.start(project=PROJECT_ID, zone=INSTANCE[1], instance=INSTANCE[0])
                    wait_for_operation(operation, "instance start")
                except Exception as err:
                    print(f'Error: {err}')
                    err_i += 1
                    continue
                print(f'\t- <{restart_i}> Instance {INSTANCE[0]} restarted.')
                if err_i > 0: err_i -= 1
                restart_i += 1
                delay *= 2
            time.sleep(5)
        time.sleep(delay)
        delay = 20


if __name__ == "__main__":
    main()
