from .logger import logger

class Worker:
    def get_next_job(self):
        raise NotImplementedError()
    
    def run_next(self):
        next_job = self.get_next_job()
        if next_job is None:
            return False
        name, fn, args, kwargs = next_job
        full_args = list()
        full_args.extend(args)
        full_args.extend(f"{k}={v}" for k,v in kwargs.items())
        args_str = ",".join(full_args)
        try:
            logger.info(f"Function: {name} is starting with arguments: {args_str}")
            fn(*args, **kwargs)
            logger.info(f"Function: {name} completed successfully.")
        except Exception as err:
            logger.error(f"Function: {name} failed to complete")
            logger.exception(err)
        return True