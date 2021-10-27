from pyrevit import EXEC_PARAMS

# hooks_logger is a helper module to provide write methods to hooks.log
# that all python hook scripts can use
import hooks_logger

# __file__ is set to the path of the hook script, per python conventions
hooks_logger.log_hook(__file__,
                      {
                          "cancellable?": str(EXEC_PARAMS.event_args.Cancellable),
                          "doc": str(EXEC_PARAMS.event_args.Document),
                          "current_view": str(EXEC_PARAMS.event_args.CurrentActiveView),
                          "prev_view": str(EXEC_PARAMS.event_args.PreviousActiveView),
                          "status": str(EXEC_PARAMS.event_args.Status),
                          }
                      )
