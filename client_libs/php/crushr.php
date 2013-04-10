<?php

/**
 * If you're in PSR-0 environment, you need to set it up to
 * load from the Crushr directory.
 * If you're not, you can include this file, and we'll set up an
 * autoloader for you. You're welcome :)
 *
 * @package 	Crushr
 * @author 		Alex Gisby <alex@solution10.com>
 * @license 	MIT
 */

spl_autoload_register(function($className)
{
    $className = ltrim($className, '\\');
    $fileName  = __DIR__ . DIRECTORY_SEPARATOR;
    $namespace = '';
    if ($lastNsPos = strrpos($className, '\\')) {
        $namespace = substr($className, 0, $lastNsPos);
        $className = substr($className, $lastNsPos + 1);
        $fileName  .= str_replace('\\', DIRECTORY_SEPARATOR, $namespace) . DIRECTORY_SEPARATOR;
    }
    $fileName .= str_replace('_', DIRECTORY_SEPARATOR, $className) . '.php';

    if(file_exists($fileName))
    {
        require $fileName;
        return true;
    }

    return false;
});
