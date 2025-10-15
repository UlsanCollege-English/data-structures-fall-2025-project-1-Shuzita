class Scheduler:
    MENU_DURATIONS = {
        "americano": 2,
        "latte": 3,
        "tea": 1,
        "mocha": 4,
        "macchiato": 2
    }

    def __init__(self):
        self.queues = {}          # queue_name -> list of tasks
        self.capacity = {}        # queue_name -> max capacity
        self.logs = []            # all logs
        self.menu = list(self.MENU_DURATIONS.keys())
        self.skip_next_turn = set()  # queues to skip only next turn
        self.task_counters = {}   # queue_name -> counter for auto task IDs

    def create_queue(self, name, cap):
        self.queues[name] = []
        self.capacity[name] = cap
        self.task_counters[name] = 1
        log = f"event=create queue={name}"
        self.logs.append(log)
        return [log]

    def enqueue(self, queue_name, item):
        logs = []
        if item not in self.menu:
            log = f"event=reject queue={queue_name} reason=unknown_item item={item}"
            self.logs.append(log)
            print("Sorry, we don't serve that.")
            return [log]

        if len(self.queues[queue_name]) >= self.capacity[queue_name]:
            log = f"event=reject queue={queue_name} reason=full item={item}"
            self.logs.append(log)
            print("Sorry, we're at capacity.")
            return [log]

        task_id = f"{queue_name}-{self.task_counters[queue_name]:03d}"
        self.task_counters[queue_name] += 1
        duration = self.MENU_DURATIONS[item]
        self.queues[queue_name].append({
            "item": item,
            "task_id": task_id,
            "remaining": duration
        })

        log = f"event=enqueue queue={queue_name} item={item} task={task_id}"
        self.logs.append(log)
        logs.append(log)
        return logs

    def run(self, quantum=1, steps=1):
        logs = []
        queue_names = list(self.queues.keys())

        if steps < 1 or steps > len(queue_names):
            log = f"event=error reason=invalid_steps steps={steps}"
            self.logs.append(log)
            logs.append(log)
            return logs

        # We will process exactly 'steps' queues in order
        for name in queue_names[:steps]:
            if self.queues[name]:
                # Check skip
                if name in self.skip_next_turn:
                    log = f"event=skip queue={name}"
                    self.logs.append(log)
                    logs.append(log)
                    self.skip_next_turn.remove(name)
                # Process the task regardless of skip
                if self.queues[name]:
                    task = self.queues[name][0]
                    task['remaining'] -= quantum
                    log = f"event=run queue={name} item={task['item']} task={task['task_id']}"
                    self.logs.append(log)
                    logs.append(log)

                    if task['remaining'] > 0:
                        log = f"event=work queue={name} item={task['item']} task={task['task_id']} remaining={task['remaining']}"
                        self.logs.append(log)
                        logs.append(log)
                    else:
                        log = f"event=finish queue={name} item={task['item']} task={task['task_id']}"
                        self.logs.append(log)
                        logs.append(log)
                        self.queues[name].pop(0)
            else:
                log = f"event=run queue={name} skipped=True"
                self.logs.append(log)
                logs.append(log)

        return logs

    def mark_skip(self, queue_name):
        self.skip_next_turn.add(queue_name)
        return [f"event=skip queue={queue_name}"]
