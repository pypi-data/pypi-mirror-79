from .logger import logger

class Worker:
    def get_next_job(self):
        raise NotImplementedError()
    
    def run_next(self):
        try:
            with self.get_next_job() as next_job:
                if next_job is None:
                    return False
                slug, fn, args, kwargs = next_job
                full_args = list()
                full_args.extend(args)
                full_args.extend(f"{k}={v}" for k,v in kwargs.items())
                args_str = ",".join(full_args)
                logger.info(f"Function: {slug} is starting with arguments: {args_str}")
                fn(*args, **kwargs)
                logger.info(f"Function: {slug} completed successfully.")
        except Exception as err:
            logger.error(f"Function: {slug} failed to complete")
            logger.exception(err)
        return True